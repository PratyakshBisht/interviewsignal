from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import httpx
from jose import jwt
from datetime import datetime, timedelta
import logging
import hashlib

from app.database import get_db
from app.models.user import User
from app.config import settings
from app.schemas.user import Token, UserResponse
from app.routers.deps import get_current_user, create_access_token

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/login/github")
async def github_login():
    """
    Get GitHub OAuth URL for authentication.
    
    Returns:
        dict: Contains authorization_url for GitHub OAuth flow
    """
    if not settings.GITHUB_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET."
        )
    
    # Generate a state parameter for CSRF protection
    state = hashlib.sha256(str(datetime.now().timestamp()).encode()).hexdigest()[:16]
    
    scope = "read:user repo"
    authorization_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.GITHUB_REDIRECT_URI}"
        f"&scope={scope}"
        f"&state={state}"
    )
    
    logger.info(f"Generated GitHub OAuth URL for client {settings.GITHUB_CLIENT_ID}")
    
    return {
        "success": True,
        "authorization_url": authorization_url,
        "method": "GET",
        "security_note": "Store the state parameter and verify it in the callback",
        "scope": scope
    }


@router.get("/callback", response_model=Token)
async def github_callback(
    code: str,
    state: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """
    GitHub OAuth callback endpoint.
    
    Args:
        code: Authorization code from GitHub
        state: State parameter for CSRF protection (optional)
        
    Returns:
        Token: JWT access token and user information
    """
    logger.info("Processing GitHub OAuth callback")
    
    # Validate required parameters
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing authorization code"
        )
    
    # 1. Exchange code for GitHub access token
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                json={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": settings.GITHUB_REDIRECT_URI
                },
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
            )
            
            token_response.raise_for_status()
            token_data = token_response.json()
            
            github_token = token_data.get("access_token")
            
            if not github_token:
                error = token_data.get("error_description", "Unknown error")
                logger.error(f"GitHub OAuth error: {error}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"GitHub authentication failed: {error}"
                )
            
            logger.info("Successfully obtained GitHub access token")
            
            # 2. Fetch GitHub user profile with the token
            user_response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            user_response.raise_for_status()
            github_profile = user_response.json()
            
            logger.info(f"Fetched GitHub profile for: {github_profile.get('login')}")
            
    except httpx.HTTPError as e:
        logger.error(f"GitHub API HTTP error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to communicate with GitHub API"
        )
    except Exception as e:
        logger.error(f"Unexpected error in GitHub callback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed due to internal error"
        )
    
    # 3. Extract user data from GitHub profile
    github_id = github_profile.get("id")
    username = github_profile.get("login")
    email = github_profile.get("email")
    avatar_url = github_profile.get("avatar_url")
    bio = github_profile.get("bio", "")
    company = github_profile.get("company", "")
    location = github_profile.get("location", "")
    
    if not github_id or not username:
        logger.error("Invalid GitHub profile data")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GitHub profile data"
        )
    
    # 4. Check if user exists in database
    query = select(User).where(User.github_id == github_id)
    result = await db.execute(query)
    existing_user = result.scalars().first()
    
    now = datetime.utcnow()
    
    # 5. Create or update user
    if not existing_user:
        # New user
        user = User(
            github_id=github_id,
            username=username,
            email=email,
            avatar_url=avatar_url,
            github_access_token=github_token,
            bio=bio,
            company=company,
            location=location,
            created_at=now,
            updated_at=now
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Created new user: {username} (ID: {user.id})")
        
    else:
        # Update existing user
        existing_user.github_access_token = github_token
        existing_user.avatar_url = avatar_url or existing_user.avatar_url
        existing_user.email = email or existing_user.email
        existing_user.bio = bio or existing_user.bio
        existing_user.company = company or existing_user.company
        existing_user.location = location or existing_user.location
        existing_user.updated_at = now
        
        await db.commit()
        await db.refresh(existing_user)
        user = existing_user
        logger.info(f"Updated existing user: {username} (ID: {user.id})")
    
    # 6. Generate JWT token for our application
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
        "github_id": user.github_id,
        "email": user.email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    }
    
    access_token = create_access_token(jwt_payload)
    
    logger.info(f"Generated JWT for user {user.username}")
    
    # 7. Return token response
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar_url": user.avatar_url,
            "github_id": user.github_id,
            "created_at": user.created_at
        },
        "message": "Authentication successful"
    }


@router.get("/userinfo", response_model=UserResponse)
async def get_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get authenticated user's information.
    
    Requires authentication.
    """
    return current_user


@router.post("/refresh")
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Refresh JWT token.
    
    Returns a new token with extended expiration.
    """
    now = datetime.utcnow()
    
    jwt_payload = {
        "sub": str(current_user.id),
        "username": current_user.username,
        "github_id": current_user.github_id,
        "email": current_user.email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    }
    
    new_token = create_access_token(jwt_payload)
    
    logger.info(f"Refreshed token for user {current_user.username}")
    
    return {
        "access_token": new_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "avatar_url": current_user.avatar_url
        }
    }


@router.post("/logout")
async def logout():
    """
    Logout endpoint.
    
    Note: JWT tokens are stateless. This endpoint serves as a 
    client-side signal to discard the token.
    """
    return {
        "success": True,
        "message": "Logout successful. Please discard your token on the client side.",
        "note": "For production, consider implementing token blacklisting or refresh token revocation."
    }


@router.get("/validate")
async def validate_token(
    current_user: User = Depends(get_current_user)
):
    """
    Validate current JWT token.
    
    Useful for checking if token is still valid.
    """
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        },
        "message": "Token is valid"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Alias for /userinfo endpoint.
    
    Returns authenticated user's profile.
    """
    return current_user

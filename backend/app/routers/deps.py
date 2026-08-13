from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import logging

from app.config import settings
from app.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/callback",
    auto_error=True,
    description="JWT Token for authentication"
)


def create_access_token(data: dict) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Payload to encode in token
        
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.APP_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.APP_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("JWT token missing 'sub' claim")
            raise credentials_exception
            
        # Verify token expiration
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
            logger.warning("JWT token expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
            
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired (ExpiredSignatureError)")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.JWTError as e:
        logger.warning(f"JWT validation error: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error in token validation: {e}")
        raise credentials_exception
    
    try:
        query = select(User).where(User.id == int(user_id))
        result = await db.execute(query)
        user = result.scalars().first()
        
        if user is None:
            logger.warning(f"User not found for ID: {user_id}")
            raise credentials_exception
        
        logger.debug(f"Authenticated user: {user.username} (ID: {user.id})")
        return user
        
    except Exception as e:
        logger.error(f"Database error during authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal authentication error"
        )


async def optional_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    """
    Get current user if token exists, otherwise return None.
    
    Useful for endpoints that allow both authenticated and unauthenticated access.
    """
    if not token:
        return None
    
    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None


# Additional dependency functions
def get_current_user_id(
    current_user: User = Depends(get_current_user)
) -> int:
    """Get current user's ID."""
    return current_user.id


def get_current_username(
    current_user: User = Depends(get_current_user)
) -> str:
    """Get current user's username."""
    return current_user.username


async def verify_admin_access(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verify user has admin access.
    
    In this version, we consider certain usernames as admin.
    In production, add proper role-based access control.
    """
    admin_usernames = ["admin", "pratyakshbisht", "superuser"]
    
    if current_user.username.lower() not in [u.lower() for u in admin_usernames]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user

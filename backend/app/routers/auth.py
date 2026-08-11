from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.user import Token

router = APIRouter()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=settings.ALGORITHM)


@router.get("/login/github")
async def github_login():
    # Frontend redirects here, we redirect to GitHub
    scope = "read:user repo"
    return {
        "url": f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_REDIRECT_URI}&scope={scope}"
    }


@router.get("/callback", response_model=Token)
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    # 1. Exchange code for GitHub Access Token
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://github.com/login/oauth/access_token",
            params={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        token_data = res.json()
        gh_token = token_data.get("access_token")

        if not gh_token:
            raise HTTPException(status_code=400, detail="Failed to get GitHub token")

        # 2. Get User Profile from GitHub
        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {gh_token}"}
        )
        gh_profile = user_res.json()

    # 3. Save or Update User in DB
    query = select(User).where(User.github_id == gh_profile["id"])
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        user = User(
            github_id=gh_profile["id"],
            username=gh_profile["login"],
            email=gh_profile.get("email"),
            avatar_url=gh_profile.get("avatar_url"),
            github_access_token=gh_token
        )
        db.add(user)
    else:
        user.github_access_token = gh_token  # Update token if changed

    await db.commit()
    await db.refresh(user)

    # 4. Generate App JWT
    jwt_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    
    return {"access_token": jwt_token, "token_type": "bearer"}

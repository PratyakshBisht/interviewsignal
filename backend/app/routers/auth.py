from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings

router = APIRouter()


@router.get("/login")
async def github_login():
    """Initiates GitHub OAuth flow"""
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.GITHUB_REDIRECT_URI}"
        f"&scope=read:user,user:email,repo"
    )
    return {"auth_url": github_auth_url}


@router.get("/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Handles GitHub OAuth callback and token exchange"""
    return {"message": "OAuth callback received", "code": code}

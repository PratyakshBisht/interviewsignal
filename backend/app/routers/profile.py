from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter()


@router.get("/{username}")
async def get_user_profile(username: str, db: AsyncSession = Depends(get_db)):
    """Retrieves user public profile and score badge"""
    return {
        "username": username,
        "name": username.title(),
        "badge": "Top 10% Developer",
        "rank": "Senior Candidate Signal",
    }

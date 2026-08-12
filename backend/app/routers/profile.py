from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.routers.deps import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile."""
    query = select(User).where(User.id == current_user.id)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user statistics."""
    query = select(Analysis)\
        .where(Analysis.user_id == current_user.id)\
        .order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    if not analyses:
        return {
            "total_analyses": 0,
            "latest_overall_score": None,
            "average_overall_score": None,
            "latest_analysis": None,
            "first_analysis": None
        }
    
    latest = analyses[0]
    avg_score = sum(a.overall_score for a in analyses) / len(analyses)
    
    return {
        "total_analyses": len(analyses),
        "latest_overall_score": latest.overall_score,
        "average_overall_score": round(avg_score, 2),
        "latest_analysis": latest.updated_at,
        "first_analysis": analyses[-1].created_at if analyses else None
    }


@router.get("/analyses/history")
async def get_analysis_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analysis history for the user."""
    query = select(Analysis)\
        .where(Analysis.user_id == current_user.id)\
        .order_by(Analysis.created_at.desc())\
        .limit(limit)
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    return [
        {
            "id": a.id,
            "overall_score": a.overall_score,
            "created_at": a.created_at,
            "scores": {
                "code_quality": a.code_quality_score,
                "consistency": a.consistency_score,
                "depth": a.depth_score,
                "production_readiness": a.production_readiness_score
            }
        }
        for a in analyses
    ]

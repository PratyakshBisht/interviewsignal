from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.routers.deps import get_current_user, verify_admin_access

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/users")
async def list_users(
    limit: int = 20,
    skip: int = 0,
    current_user: User = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin endpoint: List all users.
    
    Requires admin access.
    """
    logger.info(f"Admin {current_user.username} listing users")
    
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    user_list = []
    for user in users:
        # Get user's analysis count
        count_query = select(Analysis).where(Analysis.user_id == user.id)
        count_result = await db.execute(count_query)
        analysis_count = len(count_result.scalars().all())
        
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "github_id": user.github_id,
            "created_at": user.created_at,
            "last_analysis_at": user.last_analysis_at,
            "analysis_count": analysis_count
        })
    
    return {
        "total_users": len(user_list),
        "users": user_list,
        "pagination": {
            "limit": limit,
            "skip": skip
        }
    }


@router.get("/analyses")
async def list_all_analyses(
    limit: int = 20,
    skip: int = 0,
    current_user: User = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin endpoint: List all analyses across users.
    
    Requires admin access.
    """
    logger.info(f"Admin {current_user.username} listing all analyses")
    
    query = select(Analysis).offset(skip).limit(limit).order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    analysis_list = []
    for analysis in analyses:
        analysis_list.append({
            "id": analysis.id,
            "user_id": analysis.user_id,
            "overall_score": analysis.overall_score,
            "created_at": analysis.created_at,
            "code_quality_score": analysis.code_quality_score,
            "consistency_score": analysis.consistency_score,
            "depth_score": analysis.depth_score,
            "production_readiness_score": analysis.production_readiness_score
        })
    
    return {
        "total_analyses": len(analysis_list),
        "analyses": analysis_list,
        "pagination": {
            "limit": limit,
            "skip": skip
        }
    }


@router.get("/stats/global")
async def global_stats(
    current_user: User = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin endpoint: Global statistics.
    
    Requires admin access.
    """
    logger.info(f"Admin {current_user.username} fetching global stats")
    
    # Total users
    user_query = select(User)
    user_result = await db.execute(user_query)
    total_users = len(user_result.scalars().all())
    
    # Total analyses
    analysis_query = select(Analysis)
    analysis_result = await db.execute(analysis_query)
    total_analyses = len(analysis_result.scalars().all())
    
    # Average score
    score_query = select(Analysis.overall_score)
    score_result = await db.execute(score_query)
    scores = score_result.scalars().all()
    avg_score = sum(scores) / len(scores) if scores else 0
    
    return {
        "total_users": total_users,
        "total_analyses": total_analyses,
        "avg_analyses_per_user": round(total_analyses / max(total_users, 1), 2),
        "average_overall_score": round(avg_score, 2),
        "system_status": "operational"
    }


@router.get("/user/{user_id}/analyses")
async def get_user_analyses_admin(
    user_id: int,
    current_user: User = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin endpoint: Get all analyses for a specific user.
    
    Requires admin access.
    """
    logger.info(f"Admin {current_user.username} fetching analyses for user {user_id}")
    
    # Check if user exists
    user_query = select(User).where(User.id == user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    # Get user analyses
    query = select(Analysis).where(
        Analysis.user_id == user_id
    ).order_by(Analysis.created_at.desc())
    
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    analysis_list = []
    for analysis in analyses:
        analysis_list.append({
            "id": analysis.id,
            "overall_score": analysis.overall_score,
            "created_at": analysis.created_at,
            "code_quality_score": analysis.code_quality_score,
            "consistency_score": analysis.consistency_score,
            "depth_score": analysis.depth_score,
            "production_readiness_score": analysis.production_readiness_score,
            "total_repos": analysis.total_repos,
            "total_commits": analysis.total_commits
        })
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "github_id": user.github_id
        },
        "total_analyses": len(analyses),
        "analyses": analysis_list
    }


@router.delete("/user/{user_id}")
async def delete_user_admin(
    user_id: int,
    current_user: User = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin endpoint: Delete a user and all their analyses.
    
    Requires admin access.
    """
    logger.info(f"Admin {current_user.username} deleting user {user_id}")
    
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    # Check if user exists
    user_query = select(User).where(User.id == user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    # Delete user's analyses first (due to foreign key constraint)
    analysis_query = select(Analysis).where(Analysis.user_id == user_id)
    analysis_result = await db.execute(analysis_query)
    analyses = analysis_result.scalars().all()
    
    for analysis in analyses:
        await db.delete(analysis)
    
    # Delete user
    await db.delete(user)
    await db.commit()
    
    logger.info(f"Deleted user {user.username} (ID: {user_id}) and {len(analyses)} analyses")
    
    return {
        "success": True,
        "message": f"Deleted user {user.username} and {len(analyses)} analyses"
    }


@router.get("/system/info")
async def system_info(
    current_user: User = Depends(verify_admin_access)
):
    """
    Admin endpoint: Get system information.
    
    Requires admin access.
    """
    import sys
    import platform
    from datetime import datetime
    
    return {
        "system": {
            "platform": platform.platform(),
            "python_version": sys.version,
            "server_time": datetime.now().isoformat()
        },
        "service": {
            "name": "InterviewSignal API",
            "version": "1.0.0",
            "status": "operational"
        },
        "admin": {
            "username": current_user.username,
            "user_id": current_user.id,
            "github_id": current_user.github_id
        }
    }

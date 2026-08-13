from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.routers.deps import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/me", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user's profile.
    
    Returns:
        Complete user profile information
    """
    logger.info(f"Fetching profile for user {current_user.username}")
    return current_user


@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive statistics for current user.
    
    Returns:
        Profile statistics including analysis history
    """
    logger.info(f"Fetching stats for user {current_user.username}")
    
    # Get analysis history
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc())
    
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    if not analyses:
        return {
            "total_analyses": 0,
            "latest_overall_score": None,
            "average_overall_score": None,
            "latest_analysis": None,
            "first_analysis": None,
            "score_trend": "unknown"
        }
    
    latest = analyses[0]
    avg_score = sum(a.overall_score for a in analyses) / len(analyses)
    
    # Determine score trend
    score_trend = "stable"
    if len(analyses) >= 2:
        recent_change = analyses[0].overall_score - analyses[-1].overall_score
        if recent_change > 5:
            score_trend = "improving"
        elif recent_change < -5:
            score_trend = "declining"
    
    return {
        "total_analyses": len(analyses),
        "latest_overall_score": latest.overall_score,
        "average_overall_score": round(avg_score, 2),
        "latest_analysis": latest.updated_at,
        "first_analysis": analyses[-1].created_at,
        "score_trend": score_trend,
        "current_scores": {
            "code_quality": latest.code_quality_score,
            "consistency": latest.consistency_score,
            "depth": latest.depth_score,
            "production_readiness": latest.production_readiness_score,
            "overall": latest.overall_score
        }
    }


@router.get("/analyses/history")
async def get_analysis_history(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated analysis history for user.
    
    Args:
        limit: Number of analyses to return (default 10)
        offset: Number of analyses to skip (default 0)
        
    Returns:
        List of past analyses
    """
    logger.info(f"Fetching analysis history for user {current_user.username}")
    
    # Get total count
    count_query = select(Analysis).where(Analysis.user_id == current_user.id)
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())
    
    # Get paginated results
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    history_items = []
    for analysis in analyses:
        item = {
            "id": analysis.id,
            "overall_score": analysis.overall_score,
            "created_at": analysis.created_at,
            "scores": {
                "code_quality": analysis.code_quality_score,
                "consistency": analysis.consistency_score,
                "depth": analysis.depth_score,
                "production_readiness": analysis.production_readiness_score
            },
            "summary_preview": (analysis.recruiter_summary[:150] + "...") 
                if analysis.recruiter_summary and len(analysis.recruiter_summary) > 150 
                else analysis.recruiter_summary
        }
        history_items.append(item)
    
    return {
        "history": history_items,
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": total > offset + limit,
            "page": (offset // limit) + 1 if limit > 0 else 1
        }
    }


@router.get("/repos/summary")
async def get_repos_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get repository summary from latest analysis.
    
    Returns:
        Repository statistics and breakdown
    """
    logger.info(f"Fetching repos summary for user {current_user.username}")
    
    # Get latest analysis
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc())
    
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis or not analysis.github_data:
        raise HTTPException(
            status_code=404,
            detail="No analysis data found. Run /analysis/trigger first."
        )
    
    github_data = analysis.github_data
    repos = github_data.get("repos", [])
    
    if not repos:
        return {
            "total_repos": 0,
            "most_used_language": None,
            "repo_statistics": None
        }
    
    # Calculate language distribution
    languages = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    
    return {
        "total_repos": len(repos),
        "total_stars": sum(repo.get("stars", 0) for repo in repos),
        "total_forks": sum(repo.get("forks", 0) for repo in repos),
        "total_commits": sum(repo.get("commit_count", 0) for repo in repos),
        "most_used_language": max(languages.items(), key=lambda x: x[1])[0] if languages else None,
        "language_distribution": [
            {"language": lang, "count": count} 
            for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        ],
        "most_active_repos": [
            {
                "name": repo.get("name"),
                "language": repo.get("language"),
                "commits": repo.get("commit_count", 0),
                "stars": repo.get("stars", 0)
            }
            for repo in sorted(repos, key=lambda x: x.get("commit_count", 0), reverse=True)[:5]
        ]
    }


@router.get("/strengths")
async def get_user_strengths(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get consolidated strengths across all analyses.
    
    Returns:
        List of recurring strengths
    """
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc()).limit(5)
    
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    if not analyses:
        return {"strengths": [], "message": "No analysis data available"}
    
    # Collect strengths from recent analyses
    all_strengths = []
    for analysis in analyses:
        if analysis.strengths:
            all_strengths.extend(analysis.strengths)
    
    # Count frequency
    strength_counts = {}
    for strength in all_strengths:
        strength_counts[strength] = strength_counts.get(strength, 0) + 1
    
    return {
        "total_distinct_strengths": len(strength_counts),
        "strengths": [
            {
                "strength": item[0],
                "frequency": item[1]
            }
            for item in sorted(strength_counts.items(), key=lambda x: x[1], reverse=True)
        ],
        "most_common_strength": max(strength_counts.items(), key=lambda x: x[1])[0] if strength_counts else None
    }


@router.get("/weaknesses")
async def get_user_weaknesses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get consolidated weaknesses across all analyses.
    
    Returns:
        List of recurring weaknesses
    """
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc()).limit(5)
    
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    if not analyses:
        return {"weaknesses": [], "message": "No analysis data available"}
    
    # Collect weaknesses
    all_weaknesses = []
    for analysis in analyses:
        if analysis.weaknesses:
            all_weaknesses.extend(analysis.weaknesses)
    
    # Count frequency
    weakness_counts = {}
    for weakness in all_weaknesses:
        weakness_counts[weakness] = weakness_counts.get(weakness, 0) + 1
    
    return {
        "total_distinct_weaknesses": len(weakness_counts),
        "weaknesses": [
            {
                "weakness": item[0],
                "frequency": item[1]
            }
            for item in sorted(weakness_counts.items(), key=lambda x: x[1], reverse=True)
        ],
        "most_common_weakness": max(weakness_counts.items(), key=lambda x: x[1])[0] if weakness_counts else None
    }


@router.get("/recommendations")
async def get_user_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get consolidated recommendations across all analyses.
    
    Returns:
        List of recurring recommendations
    """
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc()).limit(5)
    
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    if not analyses:
        return {"recommendations": [], "message": "No analysis data available"}
    
    # Collect recommendations
    all_recommendations = []
    for analysis in analyses:
        if analysis.recommendations:
            all_recommendations.extend(analysis.recommendations)
    
    # Count frequency
    rec_counts = {}
    for rec in all_recommendations:
        rec_counts[rec] = rec_counts.get(rec, 0) + 1
    
    return {
        "total_distinct_recommendations": len(rec_counts),
        "recommendations": [
            {
                "recommendation": item[0],
                "frequency": item[1]
            }
            for item in sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)
        ],
        "top_recommendation": max(rec_counts.items(), key=lambda x: x[1])[0] if rec_counts else None
    }

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import logging
from typing import List, Optional, Dict, Any
import uuid

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.services.github_service import GitHubService
from app.services.scoring_engine import ScoringEngine
from app.services.llm_service import LLMService
from app.routers.deps import get_current_user
from app.schemas.analysis import AnalysisResponse, AnalysisRequest

router = APIRouter()
logger = logging.getLogger(__name__)


async def process_github_analysis(
    user: User,
    force_refresh: bool = False,
    db: AsyncSession = None
) -> Analysis:
    """
    Core analysis processing logic.
    
    Args:
        user: User object
        force_refresh: Whether to force refresh cached data
        db: Database session
        
    Returns:
        Analysis object
        
    Raises:
        Exception: If GitHub API fails
    """
    logger.info(f"Starting analysis for user {user.username}")
    
    # Fetch GitHub data
    try:
        github_data = await GitHubService.analyze_user_profile(
            user.github_access_token,
            user.username
        )
    except Exception as e:
        logger.error(f"GitHub API failed for {user.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch GitHub data"
        )
    
    if not github_data or not github_data.get("repos"):
        logger.warning(f"No GitHub data found for {user.username}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No GitHub repositories found"
        )
    
    # Calculate scores
    score_data = ScoringEngine.calculate_scores(github_data)
    
    # Generate AI summary
    llm_data = LLMService.generate_summary(github_data, score_data)
    
    # Calculate totals
    repos = github_data.get("repos", [])
    total_repos = len(repos)
    total_commits = sum(repo.get("commit_count", 0) for repo in repos)
    
    # Create analysis record
    analysis = Analysis(
        user_id=user.id,
        github_data=github_data,
        total_repos=total_repos,
        total_commits=total_commits,
        code_quality_score=score_data["code_quality_score"],
        consistency_score=score_data["consistency_score"],
        depth_score=score_data["depth_score"],
        production_readiness_score=score_data["production_readiness_score"],
        overall_score=score_data["overall_score"],
        recruiter_summary=llm_data["recruiter_summary"],
        strengths=llm_data.get("strengths", []),
        weaknesses=llm_data.get("weaknesses", []),
        recommendations=llm_data.get("recommendations", []),
        analysis_version="1.0",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    
    # Update user's last analysis time
    user.last_analysis_at = datetime.utcnow()
    await db.commit()
    
    logger.info(f"Analysis completed for {user.username}: score={analysis.overall_score}")
    return analysis


@router.post("/trigger", response_model=AnalysisResponse)
async def trigger_analysis(
    request: AnalysisRequest = AnalysisRequest(),
    background_tasks: BackgroundTasks = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger new analysis of GitHub profile.
    
    Args:
        request: AnalysisRequest with optional force_refresh flag
        background_tasks: For async processing
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Latest analysis
    """
    logger.info(f"Analysis triggered for user {current_user.username}")
    
    # Check for recent analysis (cache for 1 hour unless forced refresh)
    if not request.force_refresh:
        query = select(Analysis).where(
            Analysis.user_id == current_user.id
        ).order_by(Analysis.created_at.desc())
        
        result = await db.execute(query)
        existing = result.scalars().first()
        
        if existing and existing.updated_at:
            cache_time = timedelta(hours=1)
            if datetime.utcnow() - existing.updated_at < cache_time:
                logger.info(f"Returning cached analysis for {current_user.username}")
                return existing
    
    try:
        # Process analysis
        analysis = await process_github_analysis(
            user=current_user,
            force_refresh=request.force_refresh,
            db=db
        )
        
        return analysis
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Analysis failed for {current_user.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete analysis"
        )


@router.post("/trigger/async", response_model=dict)
async def trigger_async_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger analysis asynchronously (in background).
    
    Returns job ID immediately for status tracking.
    """
    job_id = str(uuid.uuid4())[:8]
    
    async def background_analysis():
        try:
            logger.info(f"Starting background analysis job {job_id} for {current_user.username}")
            
            async with get_db() as db_session:
                # Get fresh DB session
                user_query = select(User).where(User.id == current_user.id)
                result = await db_session.execute(user_query)
                user = result.scalars().first()
                
                analysis = await process_github_analysis(
                    user=user,
                    force_refresh=request.force_refresh,
                    db=db_session
                )
                
                logger.info(f"Background analysis completed: {job_id}")
                
        except Exception as e:
            logger.error(f"Background analysis failed {job_id}: {e}")
    
    # Start background task
    background_tasks.add_task(background_analysis)
    
    return {
        "job_id": job_id,
        "status": "started",
        "message": "Analysis started in background",
        "estimated_time": "30-60 seconds",
        "check_status_at": f"/analysis/jobs/{job_id}"
    }


@router.get("/latest", response_model=AnalysisResponse)
async def get_latest_analysis(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the most recent analysis for current user.
    
    Returns:
        Latest analysis or 404 if none found
    """
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc())
    
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No analysis found. Please run /analysis/trigger first."
        )
    
    return analysis


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_by_id(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific analysis by ID.
    
    Args:
        analysis_id: ID of analysis to retrieve
        
    Returns:
        Analysis with given ID
        
    Raises:
        HTTPException: If analysis not found or access denied
    """
    query = select(Analysis).where(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    )
    
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found or access denied."
        )
    
    return analysis


@router.get("/", response_model=dict)
async def get_analysis_history(
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated analysis history.
    
    Args:
        limit: Items per page (1-50)
        page: Page number
        
    Returns:
        Paginated analysis history
    """
    offset = (page - 1) * limit
    
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
        history_items.append({
            "id": analysis.id,
            "overall_score": analysis.overall_score,
            "created_at": analysis.created_at,
            "updated_at": analysis.updated_at,
            "scores": {
                "code_quality": analysis.code_quality_score,
                "consistency": analysis.consistency_score,
                "depth": analysis.depth_score,
                "production_readiness": analysis.production_readiness_score
            },
            "total_repos": analysis.total_repos,
            "total_commits": analysis.total_commits,
            "summary_preview": (analysis.recruiter_summary[:100] + "...") 
                if analysis.recruiter_summary else None
        })
    
    return {
        "data": history_items,
        "pagination": {
            "total": total,
            "limit": limit,
            "page": page,
            "total_pages": (total + limit - 1) // limit if limit > 0 else 1,
            "has_next": total > offset + limit,
            "has_prev": page > 1
        }
    }


@router.get("/stats/overall", response_model=dict)
async def get_overall_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive analysis statistics.
    
    Returns:
        Various statistics about user's analyses
    """
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc())
    
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    if not analyses:
        return {
            "total_analyses": 0,
            "message": "No analyses found. Run /analysis/trigger first.",
            "scores": {
                "average": 0,
                "best": 0,
                "worst": 0,
                "trend": "unknown"
            }
        }
    
    scores = [a.overall_score for a in analyses]
    
    # Calculate trends
    score_trend = "stable"
    if len(analyses) >= 2:
        first_score = analyses[-1].overall_score
        latest_score = analyses[0].overall_score
        if latest_score > first_score + 5:
            score_trend = "improving"
        elif latest_score < first_score - 5:
            score_trend = "declining"
    
    return {
        "total_analyses": len(analyses),
        "total_repos_analyzed": sum(a.total_repos for a in analyses),
        "total_commits_analyzed": sum(a.total_commits for a in analyses),
        "scores": {
            "average": round(sum(scores) / len(scores), 2),
            "best": round(max(scores), 2),
            "worst": round(min(scores), 2),
            "range": round(max(scores) - min(scores), 2),
            "trend": score_trend
        },
        "category_averages": {
            "code_quality": round(sum(a.code_quality_score for a in analyses) / len(analyses), 2),
            "consistency": round(sum(a.consistency_score for a in analyses) / len(analyses), 2),
            "depth": round(sum(a.depth_score for a in analyses) / len(analyses), 2),
            "production_readiness": round(sum(a.production_readiness_score for a in analyses) / len(analyses), 2)
        },
        "first_analysis": analyses[-1].created_at,
        "last_analysis": analyses[0].created_at
    }


@router.get("/github-data/raw", response_model=dict)
async def get_raw_github_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get raw GitHub data from latest analysis.
    
    Returns:
        Raw GitHub API data for debugging
    """
    query = select(Analysis).where(
        Analysis.user_id == current_user.id
    ).order_by(Analysis.created_at.desc())
    
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis or not analysis.github_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No GitHub data available."
        )
    
    return {
        "data": analysis.github_data,
        "analysis_id": analysis.id,
        "fetched_at": analysis.created_at
    }


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific analysis.
    
    Args:
        analysis_id: ID of analysis to delete
        
    Returns:
        204 No Content on success
    """
    query = select(Analysis).where(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    )
    
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found or access denied."
        )
    
    await db.delete(analysis)
    await db.commit()
    
    logger.info(f"Deleted analysis {analysis_id} for user {current_user.username}")


@router.get("/compare/{analysis_id_1}/{analysis_id_2}", response_model=dict)
async def compare_analyses(
    analysis_id_1: int,
    analysis_id_2: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Compare two analyses.
    
    Args:
        analysis_id_1: First analysis ID
        analysis_id_2: Second analysis ID
        
    Returns:
        Comparison data
    """
    query = select(Analysis).where(
        Analysis.id.in_([analysis_id_1, analysis_id_2]),
        Analysis.user_id == current_user.id
    )
    
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    if len(analyses) != 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both analyses not found or access denied."
        )
    
    # Sort by ID for consistency
    analyses.sort(key=lambda x: x.id)
    a1, a2 = analyses
    
    # Calculate differences
    score_diff = a2.overall_score - a1.overall_score
    
    return {
        "analysis_1": {
            "id": a1.id,
            "created_at": a1.created_at,
            "overall_score": a1.overall_score,
            "scores": {
                "code_quality": a1.code_quality_score,
                "consistency": a1.consistency_score,
                "depth": a1.depth_score,
                "production_readiness": a1.production_readiness_score
            }
        },
        "analysis_2": {
            "id": a2.id,
            "created_at": a2.created_at,
            "overall_score": a2.overall_score,
            "scores": {
                "code_quality": a2.code_quality_score,
                "consistency": a2.consistency_score,
                "depth": a2.depth_score,
                "production_readiness": a2.production_readiness_score
            }
        },
        "comparison": {
            "overall_score_change": score_diff,
            "category_changes": {
                "code_quality": a2.code_quality_score - a1.code_quality_score,
                "consistency": a2.consistency_score - a1.consistency_score,
                "depth": a2.depth_score - a1.depth_score,
                "production_readiness": a2.production_readiness_score - a1.production_readiness_score
            },
            "days_between": abs((a2.created_at - a1.created_at).days),
            "interpretation": f"Overall score {'improved' if score_diff > 0 else 'declined' if score_diff < 0 else 'stayed the same'} by {abs(score_diff):.2f} points"
        }
    }

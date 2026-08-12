from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.services.github_service import GitHubService
from app.services.scoring_engine import ScoringEngine
from app.routers.deps import get_current_user
from app.schemas.analysis import AnalysisResponse, AnalysisRequest

router = APIRouter()


@router.post("/trigger", response_model=AnalysisResponse)
async def trigger_analysis(
    request: AnalysisRequest = AnalysisRequest(),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Fetch GitHub data and trigger scoring.
    """
    if not current_user.github_access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No GitHub access token associated with this user."
        )

    # Check if we already have a recent analysis
    query = select(Analysis).where(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    existing = result.scalars().first()
    
    if existing and not request.force_refresh:
        # If analysis is less than 1 hour old, return cached version
        if existing.updated_at and (datetime.utcnow() - existing.updated_at).total_seconds() < 3600:
            return existing
    
    # Fetch fresh data from GitHub
    try:
        github_data = await GitHubService.analyze_user_profile(
            current_user.github_access_token,
            current_user.username
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GitHub data: {str(e)}")
    
    # Compute scores using the scoring engine
    score_data = ScoringEngine.calculate_scores(github_data)

    # Create or update analysis
    if existing:
        existing.github_data = github_data
        existing.code_quality_score = score_data["code_quality_score"]
        existing.consistency_score = score_data["consistency_score"]
        existing.depth_score = score_data["depth_score"]
        existing.production_readiness_score = score_data["production_readiness_score"]
        existing.overall_score = score_data["overall_score"]
        existing.strengths = score_data["strengths"]
        existing.weaknesses = score_data["weaknesses"]
        existing.recommendations = score_data["recommendations"]
        existing.updated_at = datetime.utcnow()
        analysis = existing
    else:
        analysis = Analysis(
            user_id=current_user.id,
            github_data=github_data,
            code_quality_score=score_data["code_quality_score"],
            consistency_score=score_data["consistency_score"],
            depth_score=score_data["depth_score"],
            production_readiness_score=score_data["production_readiness_score"],
            overall_score=score_data["overall_score"],
            strengths=score_data["strengths"],
            weaknesses=score_data["weaknesses"],
            recommendations=score_data["recommendations"],
        )
        db.add(analysis)
    
    await db.commit()
    await db.refresh(analysis)
    
    return analysis


@router.get("/latest", response_model=AnalysisResponse)
async def get_latest_analysis(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the latest analysis for the current user (no new fetch).
    """
    query = select(Analysis).where(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found. Run /trigger first.")
    
    return analysis


@router.get("/github-data")
async def get_raw_github_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get raw GitHub data from the latest analysis.
    """
    query = select(Analysis).where(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis or not analysis.github_data:
        raise HTTPException(status_code=404, detail="No GitHub data found.")
    
    return analysis.github_data

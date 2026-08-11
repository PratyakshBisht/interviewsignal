from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.services.github_service import GitHubService
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
    
    # Create or update analysis (scoring happens in Module 4)
    if existing:
        existing.github_data = github_data
        existing.updated_at = datetime.utcnow()
        analysis = existing
    else:
        analysis = Analysis(
            user_id=current_user.id,
            github_data=github_data,
            code_quality_score=0.0,
            consistency_score=0.0,
            depth_score=0.0,
            production_readiness_score=0.0,
            overall_score=0.0,
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

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.user import User
from app.models.analysis import Analysis
from app.services.github_service import GitHubService
from app.services.scoring_engine import ScoringEngine
from app.services.llm_service import LLMService
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
    Fetch GitHub data, compute scores, and generate AI summary.
    """
    if not current_user.github_access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No GitHub access token associated with this user."
        )

    # Check for recent analysis
    query = select(Analysis)\
        .where(Analysis.user_id == current_user.id)\
        .order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    existing = result.scalars().first()
    
    # Return cached if fresh and not forced refresh
    if existing and not request.force_refresh:
        if existing.updated_at:
            time_diff = (datetime.utcnow() - existing.updated_at).total_seconds()
            if time_diff < 3600:  # 1 hour cache
                return existing
    
    try:
        # Step 1: Fetch GitHub data
        github_data = await GitHubService.analyze_user_profile(
            current_user.github_access_token,
            current_user.username
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch GitHub data: {str(e)}"
        )
    
    # Step 2: Calculate scores
    score_data = ScoringEngine.calculate_scores(github_data)
    
    # Step 3: Generate AI summary
    llm_data = LLMService.generate_summary(github_data, score_data)
    
    # Step 4: Save to database
    if existing:
        existing.github_data = github_data
        existing.code_quality_score = score_data["code_quality_score"]
        existing.consistency_score = score_data["consistency_score"]
        existing.depth_score = score_data["depth_score"]
        existing.production_readiness_score = score_data["production_readiness_score"]
        existing.overall_score = score_data["overall_score"]
        existing.recruiter_summary = llm_data["recruiter_summary"]
        existing.strengths = llm_data.get("strengths", [])
        existing.weaknesses = llm_data.get("weaknesses", [])
        existing.recommendations = llm_data.get("recommendations", [])
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
            recruiter_summary=llm_data["recruiter_summary"],
            strengths=llm_data.get("strengths", []),
            weaknesses=llm_data.get("weaknesses", []),
            recommendations=llm_data.get("recommendations", []),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
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
    """Get the latest analysis for the current user."""
    query = select(Analysis)\
        .where(Analysis.user_id == current_user.id)\
        .order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No analysis found. Run /analysis/trigger first."
        )
    
    return analysis


@router.get("/github-data")
async def get_raw_github_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get raw GitHub data from latest analysis."""
    query = select(Analysis)\
        .where(Analysis.user_id == current_user.id)\
        .order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis or not analysis.github_data:
        raise HTTPException(
            status_code=404,
            detail="No GitHub data available."
        )
    
    return analysis.github_data


@router.get("/summary")
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get only the summary and scores."""
    query = select(Analysis)\
        .where(Analysis.user_id == current_user.id)\
        .order_by(Analysis.created_at.desc())
    result = await db.execute(query)
    analysis = result.scalars().first()
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="No analysis found."
        )
    
    return {
        "overall_score": analysis.overall_score,
        "scores": {
            "code_quality": analysis.code_quality_score,
            "consistency": analysis.consistency_score,
            "depth": analysis.depth_score,
            "production_readiness": analysis.production_readiness_score
        },
        "summary": analysis.recruiter_summary,
        "strengths": analysis.strengths,
        "weaknesses": analysis.weaknesses,
        "recommendations": analysis.recommendations,
        "last_updated": analysis.updated_at
    }

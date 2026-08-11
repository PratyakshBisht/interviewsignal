from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.analysis import AnalysisResponse, AnalysisRead
from app.services.scoring_engine import ScoringEngine
from app.services.llm_service import LLMService

router = APIRouter()


@router.post("/trigger/{username}")
async def trigger_analysis(username: str, db: AsyncSession = Depends(get_db)):
    """Triggers reputation analysis for a GitHub user"""
    scores = ScoringEngine.calculate_scores([{"name": "demo-repo", "stargazers_count": 5, "forks_count": 2}])
    summary = await LLMService.generate_recruiter_summary(username, scores)
    return {
        "status": "completed",
        "username": username,
        "scores": scores,
        "summary": summary,
    }


@router.get("/{username}")
async def get_analysis(username: str, db: AsyncSession = Depends(get_db)):
    """Fetches latest analysis for a user"""
    scores = ScoringEngine.calculate_scores([{"name": "demo-repo", "stargazers_count": 5, "forks_count": 2}])
    summary = await LLMService.generate_recruiter_summary(username, scores)
    return {
        "status": "completed",
        "username": username,
        "scores": scores,
        "summary": summary,
    }

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel


class RepoData(BaseModel):
    name: str
    language: Optional[str] = None
    stars: int = 0
    forks: int = 0
    commit_count: int = 0
    pr_count: int = 0
    issue_count: int = 0


class AnalysisBase(BaseModel):
    code_quality_score: float = 0.0
    consistency_score: float = 0.0
    depth_score: float = 0.0
    production_readiness_score: float = 0.0
    overall_score: float = 0.0


class AnalysisCreate(AnalysisBase):
    github_data: Optional[Dict[str, Any]] = None
    recruiter_summary: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None


class AnalysisResponse(AnalysisBase):
    id: int
    user_id: int
    github_data: Optional[Dict[str, Any]] = None
    recruiter_summary: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AnalysisRequest(BaseModel):
    force_refresh: bool = False

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class RepoData(BaseModel):
    name: str
    url: str
    description: Optional[str] = None
    stars: int
    forks: int
    is_fork: bool
    language: Optional[str] = None
    commit_count: int
    pr_count: int
    issue_count: int
    has_tests: bool
    has_ci: bool
    has_docs: bool


class AnalysisResponse(BaseModel):
    id: int
    user_id: int
    code_quality_score: float
    consistency_score: float
    depth_score: float
    production_readiness_score: float
    overall_score: float
    recruiter_summary: Optional[str] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalysisRequest(BaseModel):
    force_refresh: bool = False

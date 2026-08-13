from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime


class ProfileStats(BaseModel):
    total_analyses: int = 0
    latest_overall_score: Optional[float] = None
    average_overall_score: Optional[float] = None
    latest_analysis: Optional[datetime] = None
    first_analysis: Optional[datetime] = None
    score_trend: str = "unknown"
    current_scores: Optional[Dict[str, float]] = None


class AnalysisHistoryItem(BaseModel):
    id: int
    overall_score: float
    created_at: datetime
    scores: Dict[str, float]
    summary_preview: Optional[str] = None


class PaginatedHistory(BaseModel):
    history: List[AnalysisHistoryItem]
    pagination: Dict[str, int]


class RepoSummary(BaseModel):
    total_repos: int
    total_stars: int
    total_forks: int
    total_commits: int
    most_used_language: Optional[str] = None
    language_distribution: List[Dict[str, int]]
    most_active_repos: List[Dict[str, Any]]


class StrengthItem(BaseModel):
    strength: str
    frequency: int


class WeaknessItem(BaseModel):
    weakness: str
    frequency: int


class RecommendationItem(BaseModel):
    recommendation: str
    frequency: int

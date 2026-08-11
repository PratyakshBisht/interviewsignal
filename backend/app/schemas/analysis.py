from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class AnalysisBase(BaseModel):
    overall_score: float = 0.0
    quality_score: float = 0.0
    depth_score: float = 0.0
    consistency_score: float = 0.0
    summary: Optional[str] = None
    strengths: List[str] = []
    areas_for_growth: List[str] = []
    repo_breakdown: List[Dict[str, Any]] = []
    language_stats: Dict[str, Any] = {}
    status: str = "pending"


class AnalysisCreate(BaseModel):
    user_id: int


class AnalysisRead(AnalysisBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisResponse(BaseModel):
    status: str
    analysis: Optional[AnalysisRead] = None
    message: Optional[str] = None

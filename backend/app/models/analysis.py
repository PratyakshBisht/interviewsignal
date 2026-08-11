from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    quality_score: Mapped[float] = mapped_column(Float, default=0.0)
    depth_score: Mapped[float] = mapped_column(Float, default=0.0)
    consistency_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    summary: Mapped[str] = mapped_column(String, nullable=True)
    strengths: Mapped[dict] = mapped_column(JSON, default=list)
    areas_for_growth: Mapped[dict] = mapped_column(JSON, default=list)
    repo_breakdown: Mapped[dict] = mapped_column(JSON, default=list)
    language_stats: Mapped[dict] = mapped_column(JSON, default=dict)
    
    status: Mapped[str] = mapped_column(String, default="pending")  # pending, completed, failed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="analyses")

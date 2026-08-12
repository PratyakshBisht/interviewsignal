from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, JSON, ForeignKey, Text, String, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Raw GitHub data
    github_data = Column(JSON, nullable=True)
    total_repos = Column(Integer, default=0)
    total_commits = Column(Integer, default=0)
    
    # Scores (0-100)
    code_quality_score = Column(Float, default=0.0)
    consistency_score = Column(Float, default=0.0)
    depth_score = Column(Float, default=0.0)
    production_readiness_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # AI-generated summary
    recruiter_summary = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True, default=list)
    weaknesses = Column(JSON, nullable=True, default=list)
    recommendations = Column(JSON, nullable=True, default=list)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    analysis_version = Column(String(10), default="1.0")
    
    # Relations
    user = relationship("User", back_populates="analyses")
    
    # Index for efficient queries
    __table_args__ = (
        Index("idx_user_id_created_at", "user_id", "created_at"),
        Index("idx_user_id_overall_score", "user_id", "overall_score"),
    )
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, user_id={self.user_id}, overall_score={self.overall_score})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "overall_score": self.overall_score,
            "code_quality_score": self.code_quality_score,
            "consistency_score": self.consistency_score,
            "depth_score": self.depth_score,
            "production_readiness_score": self.production_readiness_score,
            "recruiter_summary": self.recruiter_summary,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recommendations": self.recommendations,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, JSON, ForeignKey, Text
from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    # GitHub data
    github_data = Column(JSON, nullable=True)
    
    # Scores
    code_quality_score = Column(Float, default=0.0)
    consistency_score = Column(Float, default=0.0)
    depth_score = Column(Float, default=0.0)
    production_readiness_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # Summary data
    recruiter_summary = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, user_id={self.user_id}, overall_score={self.overall_score})>"

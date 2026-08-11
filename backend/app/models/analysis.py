from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Raw data from GitHub
    github_data = Column(JSON)  # Stores full repo list, commit counts, etc.
    
    # Scores (0-100)
    code_quality_score = Column(Float, default=0.0)
    consistency_score = Column(Float, default=0.0)
    depth_score = Column(Float, default=0.0)
    production_readiness_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # AI Summary
    recruiter_summary = Column(String, nullable=True)
    strengths = Column(JSON, nullable=True)  # List of strength points
    weaknesses = Column(JSON, nullable=True)  # List of weakness points
    recommendations = Column(JSON, nullable=True)  # List of recommendations
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

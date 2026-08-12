from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=True, index=True)
    avatar_url = Column(Text, nullable=True)
    github_access_token = Column(Text, nullable=False)
    
    # Profile info
    bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_analysis_at = Column(DateTime, nullable=True)
    
    # Relations
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, github_id={self.github_id})>"
    
    def __str__(self):
        return f"{self.username} ({self.github_id})"

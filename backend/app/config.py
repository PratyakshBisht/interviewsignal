from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import os
from typing import Optional


class Settings(BaseSettings):
    # App Configuration
    APP_SECRET_KEY: str = Field(default="dev_secret_key_change_in_production_1234567890")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=1440)  # 24 hours
    
    # GitHub OAuth
    GITHUB_CLIENT_ID: str = Field(default="")
    GITHUB_CLIENT_SECRET: str = Field(default="")
    GITHUB_REDIRECT_URI: str = Field(default="http://localhost:8000/auth/callback")
    
    # Database
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:password@localhost:5432/interviewsignal")
    
    # Redis (optional)
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # OpenAI/Llama API (optional)
    OPENAI_API_KEY: str = Field(default="")
    OPENAI_BASE_URL: Optional[str] = Field(default=None)
    
    # Frontend URLs for CORS
    FRONTEND_URL: str = Field(default="http://localhost:5173")
    
    # App settings
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")
    
    # API rate limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")
    
    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL must be set")
        if v.startswith("sqlite"):
            return v
        if v.startswith("postgresql"):
            return v
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        return v
    
    @field_validator("APP_SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32 and not os.getenv("DEBUG", "true").lower() == "true":
            raise ValueError("APP_SECRET_KEY must be at least 32 characters in production")
        return v


# Create settings instance
settings = Settings()

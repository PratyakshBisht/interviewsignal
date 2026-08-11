from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_SECRET_KEY: str = "your_super_secret_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    GITHUB_CLIENT_ID: str = "your_github_client_id"
    GITHUB_CLIENT_SECRET: str = "your_github_client_secret"
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/interviewsignal"
    REDIS_URL: str = "redis://localhost:6379/0"

    OPENAI_API_KEY: str = ""
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Single instance used across the app
settings = Settings()

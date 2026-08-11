from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, analysis, profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (use Alembic for production migrations)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Database initialization notice: {e}")
    yield


app = FastAPI(
    title="InterviewSignal API",
    description="Developer reputation graph for students",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "InterviewSignal API"}

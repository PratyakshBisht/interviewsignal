from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from app.config import settings
from app.database import init_db, close_db
from app.routers import auth, analysis, profile, admin

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("🚀 Starting up InterviewSignal API...")
    try:
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise
    
    yield  # App runs here
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    await close_db()
    logger.info("✅ Cleanup complete")


app = FastAPI(
    title="InterviewSignal API",
    description="Developer reputation graph for students - Backend Service",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "InterviewSignal Team",
        "url": "https://github.com/pratyakshbisht/interviewsignal"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS Configuration - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint with API information."""
    return {
        "service": "InterviewSignal API",
        "version": "1.0.0",
        "description": "Developer reputation graph for students",
        "documentation": "/docs",
        "endpoints": {
            "auth": "/auth",
            "analysis": "/analysis",
            "profile": "/profile",
            "admin": "/admin"
        },
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "InterviewSignal API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    """Return OpenAPI specification."""
    return app.openapi()


# Custom exception handlers
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found.",
            "path": request.url.path,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again later.",
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

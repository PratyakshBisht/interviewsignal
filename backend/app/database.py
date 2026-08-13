from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import logging
import os

from app.config import settings

logger = logging.getLogger(__name__)


# ORM Base class
class Base(DeclarativeBase):
    pass


def get_engine(db_url: str):
    """Create async engine for given database URL."""
    is_sqlite = db_url.startswith("sqlite")
    
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    
    if is_sqlite:
        return create_async_engine(
            db_url,
            echo=settings.DEBUG,
            connect_args=connect_args,
        )
    else:
        return create_async_engine(
            db_url,
            echo=settings.DEBUG,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
        )


engine = get_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def init_db():
    """Initialize database tables with automatic SQLite fallback if PostgreSQL is down."""
    global engine, AsyncSessionLocal
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f"Database initialized successfully with URL: {settings.DATABASE_URL}")
    except Exception as e:
        # If PostgreSQL is not reachable, fall back to SQLite for seamless dev mode
        if "postgresql" in settings.DATABASE_URL:
            logger.warning(
                f"PostgreSQL connection failed ({e}). "
                "Falling back to local SQLite database for instant local development..."
            )
            fallback_url = "sqlite+aiosqlite:///./interviewsignal.db"
            settings.DATABASE_URL = fallback_url
            engine = get_engine(fallback_url)
            AsyncSessionLocal = async_sessionmaker(
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False,
            )
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Local SQLite database initialized successfully at ./interviewsignal.db")
        else:
            logger.error(f"Database initialization failed: {e}")
            raise


async def close_db():
    """Close database connection."""
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")


# Dependency for FastAPI
async def get_db():
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

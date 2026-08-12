import asyncio
import sys
from app.database import init_db, Base


async def init():
    """Initialize database schema."""
    print("Initializing database schema...")
    try:
        await init_db()
        print("✓ Database schema created successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(init())

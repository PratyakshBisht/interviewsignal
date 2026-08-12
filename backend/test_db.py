import asyncio
from app.database import AsyncSessionLocal, init_db
from app.models.user import User
from sqlalchemy.future import select


async def test_db():
    """Test database connection and operations."""
    print("Testing database connection...")
    
    # Initialize DB
    await init_db()
    print("✓ Database initialized")
    
    # Test session
    async with AsyncSessionLocal() as session:
        # Test query
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"✓ Found {len(users)} users in database")
    
    print("✓ Database test passed!")


if __name__ == "__main__":
    asyncio.run(test_db())

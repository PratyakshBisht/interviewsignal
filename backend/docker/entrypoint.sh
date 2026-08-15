#!/bin/bash
set -e

echo "🚀 Starting InterviewSignal Backend Setup..."

# Wait for PostgreSQL
if [[ "$DATABASE_URL" == "postgresql://"* || "$DATABASE_URL" == "postgres://"* ]]; then
    echo "📦 Waiting for PostgreSQL..."
    DB_HOST=$(echo $DATABASE_URL | sed -e 's|^.*@||' -e 's|:.*$||')
    DB_PORT=$(echo $DATABASE_URL | sed -e 's|^.*:||' -e 's|/.*$||')
    until pg_isready -h "$DB_HOST" -p "${DB_PORT:-5432}" 2>/dev/null; do
        echo "Waiting for PostgreSQL ($DB_HOST)..."
        sleep 2
    done
fi

# Initialize database
echo "📊 Initializing database..."
python -c "
import asyncio
from app.database import init_db

async def setup():
    try:
        await init_db()
        print('✅ Database initialized successfully')
    except Exception as e:
        print(f'⚠️ Database initialization warning: {e}')
        print('Continuing anyway...')

asyncio.run(setup())
"

# Run migrations if using Alembic
if [ -f "alembic.ini" ]; then
    echo "📝 Running database migrations..."
    alembic upgrade head || echo "⚠️ Migration step skipped or failed"
fi

# Start the application
echo "🚀 Starting FastAPI server..."
exec "$@"

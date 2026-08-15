import pytest
import httpx

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_latest_analysis_unauthorized():
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{BASE_URL}/analysis/latest")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_trigger_analysis_unauthorized():
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(f"{BASE_URL}/analysis/trigger", json={"force_refresh": True})
        assert response.status_code == 401

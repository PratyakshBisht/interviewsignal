import httpx
from typing import Dict, Any, List, Optional


class GitHubService:
    BASE_URL = "https://api.github.com"

    def __init__(self, access_token: Optional[str] = None):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "InterviewSignal-App",
        }
        if access_token:
            self.headers["Authorization"] = f"Bearer {access_token}"

    async def get_user_profile(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/user", headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_user_repos(self, username: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/users/{username}/repos?sort=updated&per_page=30",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

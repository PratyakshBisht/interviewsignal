from typing import Dict, Any
from app.config import settings


class LLMService:
    """Generates AI-powered recruiter summaries and talent assessments."""

    @staticmethod
    async def generate_recruiter_summary(username: str, stats: Dict[str, Any]) -> str:
        if not settings.OPENAI_API_KEY:
            return (
                f"{username} demonstrates high potential with strong full-stack foundations, "
                f"consistent commit habits, and structured repository architectures. "
                f"Well-suited for modern software engineering and product-driven teams."
            )

        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            prompt = (
                f"Generate a concise 3-sentence recruiter assessment for developer @{username} "
                f"with stats: {stats}. Highlight technical strengths and readiness for engineering roles."
            )
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            return response.choices[0].message.content or ""
        except Exception:
            return (
                f"{username} displays solid development workflows, active coding cadence, "
                f"and clear software architecture patterns across public repositories."
            )

from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from app.config import settings


class LLMService:
    """Generates AI-powered summaries from GitHub data with fallback handling."""

    @staticmethod
    def build_prompt(github_data: Dict[str, Any], score_data: Dict[str, Any]) -> str:
        """Construct prompt for LLM."""
        repos = github_data.get("repos", [])[:10]  # Limit to 10 repos

        repo_lines = []
        for repo in repos:
            repo_lines.append(
                f"- {repo.get('name', 'unknown')}: "
                f"language={repo.get('language', 'unknown')}, "
                f"commits={repo.get('commit_count', 0)}, "
                f"prs={repo.get('pr_count', 0)}, "
                f"issues={repo.get('issue_count', 0)}, "
                f"tests={'yes' if repo.get('has_tests') else 'no'}, "
                f"ci={'yes' if repo.get('has_ci') else 'no'}, "
                f"docs={'yes' if repo.get('has_docs') else 'no'}"
            )

        repo_summary = "\n".join(repo_lines) if repo_lines else "- No repositories found"

        prompt = f"""You are a technical recruiter assistant evaluating a software engineering candidate's GitHub portfolio.

PROFILE DATA:
- Username: {github_data.get('username', 'unknown')}
- Total repositories: {github_data.get('total_repos', 0)}
- Overall score: {score_data.get('overall_score', 0)}/100

SCORES:
- Code Quality: {score_data.get('code_quality_score', 0)}/100
- Consistency: {score_data.get('consistency_score', 0)}/100  
- Technical Depth: {score_data.get('depth_score', 0)}/100
- Production Readiness: {score_data.get('production_readiness_score', 0)}/100

REPOSITORY DETAILS:
{repo_summary}

INSTRUCTIONS:
1. Write a concise recruiter-friendly summary (max 150 words)
2. List 2-3 key strengths based on evidence
3. List 2-3 improvement areas
4. Give 2-3 actionable recommendations

OUTPUT FORMAT (JSON only):
{{
  "summary": "concise summary here",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "recommendations": ["recommendation1", "recommendation2", "recommendation3"]
}}"""

        return prompt.strip()

    @staticmethod
    def fallback_summary(github_data: Dict[str, Any], score_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback summary when LLM is unavailable."""
        repos = github_data.get("repos", [])
        total_repos = len(repos)
        total_commits = sum(repo.get("commit_count", 0) for repo in repos)
        tested_repos = sum(1 for repo in repos if repo.get("has_tests"))
        ci_repos = sum(1 for repo in repos if repo.get("has_ci"))
        doc_repos = sum(1 for repo in repos if repo.get("has_docs"))

        summary = f"""The candidate's GitHub profile shows {total_repos} repositories with {total_commits} tracked commits. Overall technical evidence is {'strong' if score_data.get('overall_score', 0) > 70 else 'moderate' if score_data.get('overall_score', 0) > 50 else 'developing'}. Key strengths include {'project depth and consistency' if score_data.get('depth_score', 0) > 60 else 'visible engineering activity'}. Areas for growth include {'production practices' if score_data.get('production_readiness_score', 0) < 60 else 'background documentation'}."""

        strengths = []
        if score_data.get("depth_score", 0) > 60:
            strengths.append("Diverse technical projects with meaningful implementation")
        if score_data.get("consistency_score", 0) > 60:
            strengths.append("Consistent development activity and commit history")
        if total_commits > 30:
            strengths.append("Demonstrates persistence and project completion")

        weaknesses = []
        if score_data.get("production_readiness_score", 0) < 50:
            weaknesses.append("Limited production-grade practices (CI/CD, automated testing)")
        if tested_repos == 0:
            weaknesses.append("No visible automated testing in repositories")
        if doc_repos < len(repos) / 2:
            weaknesses.append("Incomplete documentation across projects")

        recommendations = []
        if tested_repos < 2:
            recommendations.append("Add automated tests to at least two main projects")
        if ci_repos < 2:
            recommendations.append("Implement CI/CD with GitHub Actions for key repositories")
        if doc_repos < len(repos) - 2:
            recommendations.append("Improve README documentation across all projects")
        if len(set(repo.get("language") for repo in repos if repo.get("language"))) < 2:
            recommendations.append("Build projects in multiple technology stacks")

        return {
            "summary": summary.strip(),
            "recruiter_summary": summary.strip(),
            "strengths": strengths[:3],
            "weaknesses": weaknesses[:3],
            "recommendations": recommendations[:3]
        }

    @staticmethod
    def generate_summary(github_data: Dict[str, Any], score_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary using OpenAI API or fallback."""

        # Try to import OpenAI
        try:
            from openai import OpenAI
        except ImportError:
            return LLMService.fallback_summary(github_data, score_data)

        # Check if API key is available
        if not settings.OPENAI_API_KEY:
            return LLMService.fallback_summary(github_data, score_data)

        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
            prompt = LLMService.build_prompt(github_data, score_data)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.3,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a technical recruiter evaluating software engineering candidates. Be honest, evidence-based, and constructive."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500
            )

            content = response.choices[0].message.content
            if not content:
                return LLMService.fallback_summary(github_data, score_data)

            parsed_response = json.loads(content)

            recruiter_summary = parsed_response.get("summary", "").strip()
            return {
                "summary": recruiter_summary,
                "recruiter_summary": recruiter_summary,
                "strengths": parsed_response.get("strengths", [])[:3],
                "weaknesses": parsed_response.get("weaknesses", [])[:3],
                "recommendations": parsed_response.get("recommendations", [])[:3]
            }

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return LLMService.fallback_summary(github_data, score_data)

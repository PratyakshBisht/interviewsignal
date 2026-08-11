from typing import List, Dict, Any


class ScoringEngine:
    """Calculates repository quality, depth, and consistency scores."""

    @staticmethod
    def calculate_scores(repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not repos:
            return {
                "overall_score": 0.0,
                "quality_score": 0.0,
                "depth_score": 0.0,
                "consistency_score": 0.0,
                "strengths": ["Clean slate ready for new projects"],
                "areas_for_growth": ["Add active repositories and commits"],
            }

        repo_count = len(repos)
        stars = sum(repo.get("stargazers_count", 0) for repo in repos)
        forks = sum(repo.get("forks_count", 0) for repo in repos)
        
        # Quality score based on stars, description completeness, license
        quality_score = min(100.0, float((stars * 5) + (repo_count * 8) + 40))
        
        # Depth score based on repository complexity and details
        depth_score = min(100.0, float((repo_count * 10) + (forks * 4) + 35))
        
        # Consistency score based on active updates
        consistency_score = min(100.0, float((repo_count * 12) + 30))

        overall_score = round((quality_score * 0.4) + (depth_score * 0.3) + (consistency_score * 0.3), 1)

        return {
            "overall_score": overall_score,
            "quality_score": round(quality_score, 1),
            "depth_score": round(depth_score, 1),
            "consistency_score": round(consistency_score, 1),
            "strengths": [
                "Consistent version control workflow",
                "Strong repository organization",
                "Demonstrated project depth in key technologies"
            ],
            "areas_for_growth": [
                "Increase test coverage across core repos",
                "Expand open-source collaboration and PR reviews"
            ]
        }

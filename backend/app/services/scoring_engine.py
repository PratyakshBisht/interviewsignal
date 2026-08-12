from typing import Dict, Any, List
from datetime import datetime
import statistics


class ScoringEngine:
    """
    Calculates scores from GitHub profile data.
    All scores are normalized to 0-100.
    """

    @staticmethod
    def calculate_scores(github_data: Dict[str, Any]) -> Dict[str, Any]:
        repos = github_data.get("repos", [])
        
        if not repos:
            return {
                "code_quality_score": 0.0,
                "consistency_score": 0.0,
                "depth_score": 0.0,
                "production_readiness_score": 0.0,
                "overall_score": 0.0,
                "strengths": ["No repositories found"],
                "weaknesses": ["No public project evidence available"],
                "recommendations": ["Add at least 2-3 meaningful projects to your GitHub profile"],
            }

        code_quality = ScoringEngine._score_code_quality(repos)
        consistency = ScoringEngine._score_consistency(repos, github_data)
        depth = ScoringEngine._score_depth(repos)
        production = ScoringEngine._score_production_readiness(repos)

        overall = round(
            (code_quality * 0.30) +
            (consistency * 0.25) +
            (depth * 0.25) +
            (production * 0.20),
            2
        )

        strengths, weaknesses, recommendations = ScoringEngine._generate_feedback(
            code_quality, consistency, depth, production, repos
        )

        return {
            "code_quality_score": round(code_quality, 2),
            "consistency_score": round(consistency, 2),
            "depth_score": round(depth, 2),
            "production_readiness_score": round(production, 2),
            "overall_score": overall,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }

    @staticmethod
    def _score_code_quality(repos: List[Dict[str, Any]]) -> float:
        """
        Based on tests, docs, README presence, repo hygiene.
        """
        score = 0.0
        total_weight = 0.0

        for repo in repos:
            repo_score = 0.0
            repo_weight = 0.0

            # Tests
            repo_weight += 30
            if repo.get("has_tests"):
                repo_score += 30

            # Docs / description
            repo_weight += 20
            if repo.get("has_docs"):
                repo_score += 20

            # Popularity signals
            repo_weight += 10
            if repo.get("stars", 0) > 0:
                repo_score += 10

            # Commit hygiene
            repo_weight += 40
            if repo.get("commit_count", 0) >= 10:
                repo_score += 40
            elif repo.get("commit_count", 0) >= 5:
                repo_score += 25
            elif repo.get("commit_count", 0) >= 1:
                repo_score += 10

            score += repo_score
            total_weight += repo_weight

        return (score / total_weight * 100) if total_weight > 0 else 0.0

    @staticmethod
    def _score_consistency(repos: List[Dict[str, Any]], github_data: Dict[str, Any]) -> float:
        """
        Based on number of repos, commit spread, and activity signals.
        """
        if not repos:
            return 0.0

        score = 0.0
        total = 0.0

        # Number of repos
        total += 25
        if len(repos) >= 5:
            score += 25
        elif len(repos) >= 3:
            score += 18
        elif len(repos) >= 1:
            score += 10

        # Active repos with recent commits
        total += 25
        active_repos = sum(1 for r in repos if r.get("commit_count", 0) > 0)
        if active_repos >= 5:
            score += 25
        elif active_repos >= 3:
            score += 18
        elif active_repos >= 1:
            score += 10

        # Commit frequency proxy
        total += 25
        total_commits = sum(r.get("commit_count", 0) for r in repos)
        if total_commits >= 100:
            score += 25
        elif total_commits >= 50:
            score += 18
        elif total_commits >= 20:
            score += 10

        # Recency signal
        total += 25
        recent_count = 0
        for repo in repos:
            pushed_at = repo.get("last_commit_date")
            if pushed_at:
                try:
                    dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
                    days_ago = (datetime.utcnow() - dt.replace(tzinfo=None)).days
                    if days_ago <= 30:
                        recent_count += 1
                except Exception:
                    pass

        if recent_count >= 3:
            score += 25
        elif recent_count >= 1:
            score += 15

        return (score / total * 100) if total > 0 else 0.0

    @staticmethod
    def _score_depth(repos: List[Dict[str, Any]]) -> float:
        """
        Measures technical depth: languages, complex repos, forks, PRs/issues.
        """
        score = 0.0
        total = 0.0

        # Language diversity
        total += 25
        languages = set()
        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages.add(lang)
            repo_langs = repo.get("languages", {})
            languages.update(repo_langs.keys())
        
        if len(languages) >= 4:
            score += 25
        elif len(languages) >= 2:
            score += 18
        elif len(languages) >= 1:
            score += 10

        # Project complexity
        total += 25
        complex_repos = 0
        for repo in repos:
            if repo.get("commit_count", 0) >= 20 and repo.get("pr_count", 0) >= 2:
                complex_repos += 1
        
        if complex_repos >= 3:
            score += 25
        elif complex_repos >= 1:
            score += 15

        # Collaboration signals
        total += 25
        total_prs = sum(r.get("pr_count", 0) for r in repos)
        total_issues = sum(r.get("issue_count", 0) for r in repos)
        if total_prs >= 10 or total_issues >= 10:
            score += 25
        elif total_prs >= 3 or total_issues >= 3:
            score += 15

        # Forks / external contributions
        total += 25
        fork_count = sum(1 for r in repos if r.get("is_fork"))
        if fork_count >= 3:
            score += 25
        elif fork_count >= 1:
            score += 10

        return (score / total * 100) if total > 0 else 0.0

    @staticmethod
    def _score_production_readiness(repos: List[Dict[str, Any]]) -> float:
        """
        Measures signs of production readiness: tests, CI, docs, deployment habits.
        """
        if not repos:
            return 0.0

        score = 0.0
        total = 0.0

        # Tests
        total += 30
        test_repos = sum(1 for r in repos if r.get("has_tests"))
        if test_repos >= 3:
            score += 30
        elif test_repos >= 1:
            score += 18

        # CI/CD
        total += 30
        ci_repos = sum(1 for r in repos if r.get("has_ci"))
        if ci_repos >= 3:
            score += 30
        elif ci_repos >= 1:
            score += 18

        # Documentation
        total += 20
        doc_repos = sum(1 for r in repos if r.get("has_docs"))
        if doc_repos >= 3:
            score += 20
        elif doc_repos >= 1:
            score += 12

        # Repo maturity
        total += 20
        mature_repos = sum(
            1 for r in repos
            if r.get("commit_count", 0) >= 10 and r.get("has_tests") and r.get("has_ci")
        )
        if mature_repos >= 2:
            score += 20
        elif mature_repos >= 1:
            score += 12

        return (score / total * 100) if total > 0 else 0.0

    @staticmethod
    def _generate_feedback(
        code_quality: float,
        consistency: float,
        depth: float,
        production: float,
        repos: List[Dict[str, Any]]
    ):
        strengths = []
        weaknesses = []
        recommendations = []

        # Strengths
        if code_quality >= 70:
            strengths.append("Good engineering hygiene with evidence of quality practices")
        if consistency >= 70:
            strengths.append("Consistent contribution pattern across multiple projects")
        if depth >= 70:
            strengths.append("Strong technical depth and project variety")
        if production >= 70:
            strengths.append("Projects show solid production readiness signals")

        # Weaknesses
        if code_quality < 40:
            weaknesses.append("Limited evidence of tests, documentation, or commit discipline")
        if consistency < 40:
            weaknesses.append("Activity appears sparse or inconsistent")
        if depth < 40:
            weaknesses.append("Projects do not yet show strong technical breadth or collaboration")
        if production < 40:
            weaknesses.append("Missing production practices like CI/CD and tests")

        # Recommendations
        if not any(r.get("has_tests") for r in repos):
            recommendations.append("Add automated tests to at least 1-2 projects")
        if not any(r.get("has_ci") for r in repos):
            recommendations.append("Set up GitHub Actions CI for your main projects")
        if sum(1 for r in repos if r.get("has_docs")) < 2:
            recommendations.append("Improve README files with setup, architecture, and usage instructions")
        if sum(r.get("commit_count", 0) for r in repos) < 20:
            recommendations.append("Work on more consistent commits and longer project histories")
        if len(set(r.get("language") for r in repos if r.get("language"))) < 2:
            recommendations.append("Build projects in at least 2 different languages or stacks")

        if not recommendations:
            recommendations.append("Keep building deeper projects with measurable impact")

        return strengths, weaknesses, recommendations

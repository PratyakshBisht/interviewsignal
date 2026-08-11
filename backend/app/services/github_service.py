from typing import Dict, List, Any
import httpx
from app.config import settings


class GitHubService:
    BASE_URL = "https://api.github.com"

    @staticmethod
    async def get_user_repos(access_token: str) -> List[Dict[str, Any]]:
        """Fetch all repos for the authenticated user."""
        repos = []
        page = 1
        
        async with httpx.AsyncClient() as client:
            while True:
                res = await client.get(
                    f"{GitHubService.BASE_URL}/user/repos",
                    params={"page": page, "per_page": 100, "sort": "updated"},
                    headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github.v3+json"}
                )
                res.raise_for_status()
                data = res.json()
                
                if not data:
                    break
                
                repos.extend(data)
                page += 1
        
        return repos

    @staticmethod
    async def get_repo_commits(owner: str, repo: str, access_token: str) -> List[Dict[str, Any]]:
        """Fetch commit history for a repo."""
        commits = []
        page = 1
        
        async with httpx.AsyncClient() as client:
            while True:
                res = await client.get(
                    f"{GitHubService.BASE_URL}/repos/{owner}/{repo}/commits",
                    params={"page": page, "per_page": 100},
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                if res.status_code == 404:
                    break  # Repo deleted or private access denied
                
                res.raise_for_status()
                data = res.json()
                
                if not data:
                    break
                
                commits.extend(data)
                page += 1
        
        return commits

    @staticmethod
    async def get_repo_languages(owner: str, repo: str, access_token: str) -> Dict[str, int]:
        """Fetch language breakdown for a repo."""
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{GitHubService.BASE_URL}/repos/{owner}/{repo}/languages",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            res.raise_for_status()
            return res.json()

    @staticmethod
    async def get_repo_pulls(owner: str, repo: str, access_token: str) -> List[Dict[str, Any]]:
        """Fetch all PRs (open and closed) for a repo."""
        prs = []
        
        async with httpx.AsyncClient() as client:
            for state in ["open", "closed"]:
                page = 1
                while True:
                    res = await client.get(
                        f"{GitHubService.BASE_URL}/repos/{owner}/{repo}/pulls",
                        params={"state": state, "page": page, "per_page": 100},
                        headers={"Authorization": f"Bearer {access_token}"}
                    )
                    
                    if res.status_code == 404:
                        break
                    
                    res.raise_for_status()
                    data = res.json()
                    
                    if not data:
                        break
                    
                    prs.extend(data)
                    page += 1
        
        return prs

    @staticmethod
    async def get_repo_issues(owner: str, repo: str, access_token: str) -> List[Dict[str, Any]]:
        """Fetch all issues for a repo."""
        issues = []
        page = 1
        
        async with httpx.AsyncClient() as client:
            while True:
                res = await client.get(
                    f"{GitHubService.BASE_URL}/repos/{owner}/{repo}/issues",
                    params={"state": "all", "page": page, "per_page": 100},
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                if res.status_code == 404:
                    break
                
                res.raise_for_status()
                data = res.json()
                
                if not data:
                    break
                
                issues.extend(data)
                page += 1
        
        return issues

    @staticmethod
    async def analyze_user_profile(access_token: str, username: str) -> Dict[str, Any]:
        """Main orchestrator: fetch all data and aggregate it."""
        repos = await GitHubService.get_user_repos(access_token)
        
        aggregated_data = {
            "username": username,
            "total_repos": len(repos),
            "repos": []
        }
        
        for repo in repos:
            repo_owner = repo["owner"]["login"]
            repo_name = repo["name"]
            
            try:
                commits = await GitHubService.get_repo_commits(repo_owner, repo_name, access_token)
                languages = await GitHubService.get_repo_languages(repo_owner, repo_name, access_token)
                prs = await GitHubService.get_repo_pulls(repo_owner, repo_name, access_token)
                issues = await GitHubService.get_repo_issues(repo_owner, repo_name, access_token)
                
                repo_data = {
                    "name": repo_name,
                    "url": repo["html_url"],
                    "description": repo.get("description"),
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "is_fork": repo["fork"],
                    "language": repo.get("language"),
                    "languages": languages,
                    "commit_count": len(commits),
                    "pr_count": len(prs),
                    "issue_count": len(issues),
                    "has_tests": await GitHubService._check_has_tests(repo_owner, repo_name, access_token),
                    "has_ci": await GitHubService._check_has_ci(repo_owner, repo_name, access_token),
                    "has_docs": repo.get("description") is not None and len(repo.get("description", "")) > 50,
                    "last_commit_date": repo.get("pushed_at"),
                    "created_at": repo.get("created_at"),
                }
                
                aggregated_data["repos"].append(repo_data)
            
            except Exception as e:
                # Skip repos we can't access
                print(f"Error fetching data for {repo_name}: {e}")
                continue
        
        return aggregated_data

    @staticmethod
    async def _check_has_tests(owner: str, repo: str, access_token: str) -> bool:
        """Check if repo has test files (pytest, jest, etc.)."""
        test_patterns = ["test_", "_test.py", ".test.js", ".spec.js", "__tests__"]
        
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(
                    f"{GitHubService.BASE_URL}/repos/{owner}/{repo}/git/trees/main?recursive=1",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                if res.status_code == 404:
                    # Try master branch
                    res = await client.get(
                        f"{GitHubService.BASE_URL}/repos/{owner}/{repo}/git/trees/master?recursive=1",
                        headers={"Authorization": f"Bearer {access_token}"}
                    )
                
                if res.status_code == 200:
                    tree = res.json().get("tree", [])
                    for item in tree:
                        if any(pattern in item.get("path", "") for pattern in test_patterns):
                            return True
            except Exception:
                pass
        
        return False

    @staticmethod
    async def _check_has_ci(owner: str, repo: str, access_token: str) -> bool:
        """Check if repo has CI/CD setup (GitHub Actions, etc.)."""
        ci_files = [".github/workflows/", ".gitlab-ci.yml", ".travis.yml", "Jenkinsfile"]
        
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(
                    f"{GitHubService.BASE_URL}/repos/{owner}/{repo}/git/trees/main?recursive=1",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                if res.status_code == 404:
                    res = await client.get(
                        f"{GitHubService.BASE_URL}/repos/{owner}/{repo}/git/trees/master?recursive=1",
                        headers={"Authorization": f"Bearer {access_token}"}
                    )
                
                if res.status_code == 200:
                    tree = res.json().get("tree", [])
                    for item in tree:
                        if any(ci_file in item.get("path", "") for ci_file in ci_files):
                            return True
            except Exception:
                pass
        
        return False

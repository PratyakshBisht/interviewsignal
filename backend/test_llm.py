import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.llm_service import LLMService

# Mock data for testing
test_github_data = {
    "username": "pratyakshbisht",
    "total_repos": 8,
    "repos": [
        {
            "name": "secure-ai-guardian",
            "language": "Python",
            "commit_count": 45,
            "pr_count": 12,
            "issue_count": 8,
            "has_tests": True,
            "has_ci": True,
            "has_docs": True
        },
        {
            "name": "interviewsignal",
            "language": "Python",
            "commit_count": 32,
            "pr_count": 5,
            "issue_count": 3,
            "has_tests": True,
            "has_ci": False,
            "has_docs": True
        }
    ]
}

test_score_data = {
    "code_quality_score": 78.5,
    "consistency_score": 82.0,
    "depth_score": 85.0,
    "production_readiness_score": 65.0,
    "overall_score": 77.6
}


def test_llm_service():
    """Test LLM service."""
    print("Testing LLM Service...")
    
    # Test fallback
    result = LLMService.fallback_summary(test_github_data, test_score_data)
    print("\nFallback Summary:")
    print(f"Summary: {result['summary'][:100]}...")
    print(f"Strengths: {result['strengths']}")
    print(f"Weaknesses: {result['weaknesses']}")
    print(f"Recommendations: {result['recommendations']}")
    
    # Test prompt building
    prompt = LLMService.build_prompt(test_github_data, test_score_data)
    print(f"\nPrompt length: {len(prompt)} characters")
    
    # Test full generation
    print("\nTesting full generation...")
    full_result = LLMService.generate_summary(test_github_data, test_score_data)
    print(f"Generated summary: {full_result['recruiter_summary'][:150]}...")
    print(f"Strengths: {full_result.get('strengths', [])}")
    print(f"Weaknesses: {full_result.get('weaknesses', [])}")
    
    return True


if __name__ == "__main__":
    test_llm_service()

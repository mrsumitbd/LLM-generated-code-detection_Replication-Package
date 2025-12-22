from typing import Any
import requests
from bs4 import BeautifulSoup
import re
import json

class LeetCodeScraper:

    def __init__(self):
        self.base_url = "https://leetcode.com"
        self.graphql_url = "https://leetcode.com/graphql"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_problem_by_slug(self, problem_slug: str) -> dict[str, Any] | None:
        query = """
        query getProblem($slug: String!) {
            problem(slug: $slug) {
                questionId
                questionFrontendId
                title
                titleSlug
                difficulty
                description
                exampleTestcases
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                topicTags {
                    name
                    slug
                }
            }
        }
        """
        variables = {"slug": problem_slug}
        
        try:
            response = self.session.post(
                self.graphql_url,
                json={"query": query, "variables": variables},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("errors"):
                return None
            
            problem = data.get("data", {}).get("problem")
            return problem if problem else None
        except Exception:
            return None

    def get_problem_by_number(self, problem_number: int) -> dict[str, Any] | None:
        slug = self._get_slug_by_number(problem_number)
        if slug:
            return self.get_problem_by_slug(slug)
        
        result = self._try_common_slugs(problem_number)
        return result

    def _get_slug_by_number(self, problem_number: int) -> str | None:
        query = """
        query getProblems {
            allQuestionsCount {
                totalQuestions
            }
            questionList(skip: 0, limit: 10000, filters: {}) {
                data {
                    frontendQuestionId
                    titleSlug
                }
            }
        }
        """
        
        try:
            response = self.session.post(
                self.graphql_url,
                json={"query": query},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            questions = data.get("data", {}).get("questionList", {}).get("data", [])
            
            for question in questions:
                if int(question.get("frontendQuestionId", 0)) == problem_number:
                    return question.get("titleSlug")
            
            return None
        except Exception:
            return None

    def _try_common_slugs(self, problem_number: int) -> dict[str, Any] | None:
        common_patterns = [
            f"problem-{problem_number}",
            f"{problem_number}",
        ]
        
        for pattern in common_patterns:
            result = self.get_problem_by_slug(pattern)
            if result:
                return result
        
        return None

    def get_python_code(self, problem_info: dict[str, Any]) -> str | None:
        if not problem_info:
            return None
        
        code_snippets = problem_info.get("codeSnippets", [])
        
        for snippet in code_snippets:
            if snippet.get("langSlug") == "python3" or snippet.get("lang") == "Python3":
                return snippet.get("code")
        
        for snippet in code_snippets:
            if snippet.get("langSlug") == "python" or snippet.get("lang") == "Python":
                return snippet.get("code")
        
        return None

    def format_problem_info(self, problem_info: dict[str, Any]) -> dict[str, Any]:
        if not problem_info:
            return {}
        
        topics = [tag.get("name") for tag in problem_info.get("topicTags", [])]
        
        formatted = {
            "id": problem_info.get("questionFrontendId"),
            "title": problem_info.get("title"),
            "slug": problem_info.get("titleSlug"),
            "difficulty": problem_info.get("difficulty"),
            "description": problem_info.get("description"),
            "topics": topics,
            "examples": problem_info.get("exampleTestcases", ""),
            "python_code": self.get_python_code(problem_info)
        }
        
        return formatted
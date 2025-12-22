import requests
from typing import Any, Optional, Dict

class LeetCodeScraper:
    def __init__(self):
        self.base_url = "https://leetcode.com/api/problems/all/"

    def get_problem_by_slug(self, problem_slug: str) -> Optional[Dict[str, Any]]:
        problem_info = self._get_problem_info(problem_slug)
        if problem_info:
            return self.format_problem_info(problem_info)
        return None

    def get_problem_by_number(self, problem_number: int) -> Optional[Dict[str, Any]]:
        problem_slug = self._get_slug_by_number(problem_number)
        if problem_slug:
            return self.get_problem_by_slug(problem_slug)
        return self._try_common_slugs(problem_number)

    def _get_slug_by_number(self, problem_number: int) -> Optional[str]:
        response = requests.get(self.base_url)
        if response.status_code == 200:
            data = response.json()
            for problem in data["stat_status_pairs"]:
                if problem["stat"]["frontend_id"] == problem_number:
                    return problem["stat"]["question__title_slug"]
        return None

    def _try_common_slugs(self, problem_number: int) -> Optional[Dict[str, Any]]:
        common_slugs = [
            f"problem-{problem_number}",
            f"p{problem_number}",
            f"lc{problem_number}",
        ]
        for slug in common_slugs:
            problem_info = self._get_problem_info(slug)
            if problem_info:
                return self.format_problem_info(problem_info)
        return None

    def _get_problem_info(self, problem_slug: str) -> Optional[Dict[str, Any]]:
        url = f"https://leetcode.com/problems/{problem_slug}/description/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def get_python_code(self, problem_info: Dict[str, Any]) -> Optional[str]:
        if "code_snippets" in problem_info:
            for snippet in problem_info["code_snippets"]:
                if snippet["lang"] == "python":
                    return snippet["code"]
        return None

    def format_problem_info(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": problem_info["question__title"],
            "difficulty": problem_info["difficulty"],
            "description": problem_info["question__description"],
            "code": self.get_python_code(problem_info),
        }
import json
import re
from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup


class LeetCodeScraper:
    """
    A lightweight scraper for LeetCode problems.
    """

    _GRAPHQL_URL = "https://leetcode.com/graphql"
    _HEADERS = {
        "User-Agent": "Mozilla/5.0 (compatible; LeetCodeScraper/1.0)",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(self._HEADERS)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_problem_by_slug(self, problem_slug: str) -> Optional[Dict[str, Any]]:
        """
        Fetch problem data by its slug.
        """
        query = """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            title
            titleSlug
            content
            difficulty
            topicTags {
              name
              slug
            }
          }
        }
        """
        payload = {"query": query, "variables": {"titleSlug": problem_slug}}
        resp = self.session.post(self._GRAPHQL_URL, json=payload)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if "errors" in data:
            return None
        return data.get("data", {}).get("question")

    def get_problem_by_number(self, problem_number: int) -> Optional[Dict[str, Any]]:
        """
        Fetch problem data by its numeric ID.
        """
        slug = self._get_slug_by_number(problem_number)
        if not slug:
            # Try common slug patterns
            return self._try_common_slugs(problem_number)
        return self.get_problem_by_slug(slug)

    def get_python_code(self, problem_info: Dict[str, Any]) -> Optional[str]:
        """
        Extract the first Python code snippet from the problem description.
        """
        content = problem_info.get("content", "")
        if not content:
            return None
        soup = BeautifulSoup(content, "html.parser")
        # LeetCode uses <pre> tags with class containing "lang-python"
        pre_tags = soup.find_all("pre", class_=re.compile(r"lang-python"))
        if not pre_tags:
            # Fallback: any <pre> that contains a Python keyword
            pre_tags = [
                pre
                for pre in soup.find_all("pre")
                if re.search(r"\bdef\b|\bclass\b", pre.text)
            ]
        if not pre_tags:
            return None
        # Clean up the code: remove leading/trailing whitespace
        code = pre_tags[0].get_text()
        return code.strip()

    def format_problem_info(self, problem_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return a simplified dictionary with selected fields.
        """
        if not problem_info:
            return {}
        formatted: Dict[str, Any] = {
            "id": problem_info.get("questionId"),
            "title": problem_info.get("title"),
            "slug": problem_info.get("titleSlug"),
            "difficulty": problem_info.get("difficulty"),
            "description": problem_info.get("content"),
            "tags": [t["name"] for t in problem_info.get("topicTags", [])],
            "python_code": self.get_python_code(problem_info),
        }
        return formatted

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _get_slug_by_number(self, problem_number: int) -> Optional[str]:
        """
        Resolve a problem number to its slug via GraphQL.
        """
        query = """
        query getQuestionDetailById($questionId: Int!) {
          question(questionId: $questionId) {
            titleSlug
          }
        }
        """
        payload = {"query": query, "variables": {"questionId": problem_number}}
        resp = self.session.post(self._GRAPHQL_URL, json=payload)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if "errors" in data:
            return None
        return data.get("data", {}).get("question", {}).get("titleSlug")

    def _try_common_slugs(self, problem_number: int) -> Optional[Dict[str, Any]]:
        """
        Attempt to fetch a problem using common slug patterns.
        """
        # Common patterns: "problem-<number>", "<number>-problem"
        patterns = [
            f"problem-{problem_number}",
            f"{problem_number}-problem",
            f"{problem_number}",
        ]
        for slug in patterns:
            prob = self.get_problem_by_slug(slug)
            if prob:
                return prob
        return None
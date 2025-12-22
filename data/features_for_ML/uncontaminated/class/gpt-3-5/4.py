from typing import Any

class LeetCodeScraper:

    def __init__(self):
        pass

    def get_problem_by_slug(self, problem_slug: str) -> dict[str, Any] | None:
        pass

    def get_problem_by_number(self, problem_number: int) -> dict[str, Any] | None:
        pass

    def _get_slug_by_number(self, problem_number: int) -> str | None:
        pass

    def _try_common_slugs(self, problem_number: int) -> dict[str, Any] | None:
        pass

    def get_python_code(self, problem_info: dict[str, Any]) -> str | None:
        pass

    def format_problem_info(self, problem_info: dict[str, Any]) -> dict[str, Any]:
        pass
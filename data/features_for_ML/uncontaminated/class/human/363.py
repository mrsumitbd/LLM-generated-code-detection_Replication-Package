from tiny_scientist.budget_checker import BudgetChecker
from typing import Any, Dict, Optional

class BaseTool:
    def __init__(self, cost_tracker: Optional[BudgetChecker] = None) -> None:
        self.cost_tracker = cost_tracker or BudgetChecker()
        self.github_token = config.get("core", {}).get("github_token")

    def run(self, *args: Any, **kwargs: Any) -> Dict[str, Dict[str, str]]:
        raise NotImplementedError
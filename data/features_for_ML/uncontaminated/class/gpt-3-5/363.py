from typing import Optional, Any, Dict
from budget_checker import BudgetChecker

class BaseTool:

    def __init__(self, cost_tracker: Optional[BudgetChecker] = None) -> None:
        self.cost_tracker = cost_tracker

    def run(self, *args: Any, **kwargs: Any) -> Dict[str, Dict[str, str]]:
        result = {}
        # Perform some operations here
        return result
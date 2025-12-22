from typing import Any, Dict, Optional

class BudgetChecker:
    def __init__(self, budget: float) -> None:
        self.budget = budget

    def check_budget(self, cost: float) -> bool:
        return cost <= self.budget

class BaseTool:
    def __init__(self, cost_tracker: Optional[BudgetChecker] = None) -> None:
        self.cost_tracker = cost_tracker

    def run(self, *args: Any, **kwargs: Any) -> Dict[str, Dict[str, str]]:
        result = {}
        for arg in args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    if self.cost_tracker and not self.cost_tracker.check_budget(value):
                        result[key] = {"status": "failed", "reason": "Budget exceeded"}
                    else:
                        result[key] = {"status": "success", "result": str(value)}
        return result
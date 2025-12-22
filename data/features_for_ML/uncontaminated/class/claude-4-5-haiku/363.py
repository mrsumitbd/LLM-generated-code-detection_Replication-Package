class BaseTool:

    def __init__(self, cost_tracker: Optional[BudgetChecker] = None) -> None:
        self.cost_tracker = cost_tracker

    def run(self, *args: Any, **kwargs: Any) -> Dict[str, Dict[str, str]]:
        return {}
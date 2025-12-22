from typing import Any, Dict, Optional

class BaseTool:
    """
    Base class for tools that can optionally track costs via a BudgetChecker.
    """

    def __init__(self, cost_tracker: Optional[Any] = None) -> None:
        """
        Initialize the tool.

        Parameters
        ----------
        cost_tracker : Optional[Any]
            An optional object responsible for tracking and enforcing budget limits.
            It is stored for use by subclasses that need to check costs.
        """
        self.cost_tracker = cost_tracker

    def run(self, *args: Any, **kwargs: Any) -> Dict[str, Dict[str, str]]:
        """
        Execute the tool's main functionality.

        Subclasses should override this method to provide concrete behavior.
        The default implementation raises a NotImplementedError.

        Returns
        -------
        Dict[str, Dict[str, str]]
            A nested dictionary containing the tool's output.
        """
        raise NotImplementedError("Subclasses must implement the run method.")
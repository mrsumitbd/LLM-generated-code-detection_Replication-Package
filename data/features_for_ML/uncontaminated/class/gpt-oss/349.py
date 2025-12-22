from typing import List, Any


class SEDTask:
    """Placeholder for the actual SEDTask implementation."""
    def __init__(self):
        self.name = "SEDTask"


class Problem:
    def create_task(self) -> SEDTask:
        """Create and return a new SEDTask instance."""
        return SEDTask()

    @property
    def train_samples(self) -> List[Any]:
        """Return a list of training samples."""
        return []

    @property
    def test_samples(self) -> List[Any]:
        """Return a list of test samples."""
        return []

    @property
    def ood_test_samples(self) -> List[Any]:
        """Return a list of out‑of‑distribution test samples."""
        return []
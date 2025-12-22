from typing import Any, Iterator, Tuple
from datasets import load_dataset, Dataset


class SimpleDatasetEnvironment:
    """
    A minimal environment that iterates over a Hugging Face dataset.
    Each call to `step` returns the next example until `max_turns` or the
    dataset is exhausted. The `reset` method restarts the iteration.
    """

    def __init__(self, dataset: Dataset, max_turns: int) -> None:
        self.dataset = dataset
        self.max_turns = max_turns
        self._reset_state()

    def _reset_state(self) -> None:
        self._index = 0
        self._done = False

    def reset(self) -> Any:
        """
        Reset the environment to the beginning of the dataset.
        Returns the first example.
        """
        self._reset_state()
        if len(self.dataset) == 0:
            self._done = True
            return None
        return self.dataset[self._index]

    def step(self, action: Any = None) -> Tuple[Any, bool]:
        """
        Advance to the next example in the dataset.

        Parameters
        ----------
        action : Any, optional
            Ignored. Included for API compatibility with RL environments.

        Returns
        -------
        observation : Any
            The next example from the dataset.
        done : bool
            True if the environment has reached `max_turns` or the end of
            the dataset; otherwise False.
        """
        if self._done:
            return None, True

        # Move to the next example
        self._index += 1

        # Check termination conditions
        if (
            self._index >= self.max_turns
            or self._index >= len(self.dataset)
        ):
            self._done = True
            return None, True

        return self.dataset[self._index], False


def load_environment(
    dataset_name: str = "math",
    dataset_split: str = "train",
    num_train_examples: int = -1,
    max_turns: int = 100,
    **kwargs,
) -> SimpleDatasetEnvironment:
    """
    Load a Hugging Face dataset and wrap it in a simple environment.

    Parameters
    ----------
    dataset_name : str, default="math"
        The name of the dataset to load.
    dataset_split : str, default="train"
        The split of the dataset to use.
    num_train_examples : int, default=-1
        If positive, only the first `num_train_examples` examples are kept.
        If negative or zero, all examples in the split are used.
    max_turns : int, default=100
        The maximum number of steps (examples) the environment will
        provide before terminating.
    **kwargs
        Additional keyword arguments passed to `datasets.load_dataset`.

    Returns
    -------
    SimpleDatasetEnvironment
        An environment that yields examples from the dataset.
    """
    # Load the dataset
    dataset = load_dataset(dataset_name, split=dataset_split, **kwargs)

    # Optionally limit the number of examples
    if num_train_examples > 0:
        dataset = dataset.select(range(min(num_train_examples, len(dataset))))

    # Create and return the environment
    return SimpleDatasetEnvironment(dataset, max_turns)
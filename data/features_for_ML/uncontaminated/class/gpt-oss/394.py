import json
import os
from typing import List, Dict, Tuple, Iterator, Any


class HelpSteer3Dataset:
    """HelpSteer3 preference dataset for DPO training."""

    def __init__(self, path: str | None = None) -> None:
        """
        Load the HelpSteer3 dataset from a JSONL file.

        Parameters
        ----------
        path : str | None, optional
            Path to the JSONL file. If None, the class will look for a file named
            ``helpsteer3.jsonl`` in the current working directory.
        """
        if path is None:
            path = os.path.join(os.getcwd(), "helpsteer3.jsonl")

        if not os.path.isfile(path):
            raise FileNotFoundError(f"HelpSteer3 dataset file not found: {path}")

        self._data: List[Dict[str, Any]] = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON line: {line}") from exc

                # Basic validation of required keys
                if not all(k in entry for k in ("prompt", "chosen", "rejected")):
                    raise ValueError(f"Missing required keys in entry: {entry}")

                self._data.append(entry)

        self._length = len(self._data)

    def __len__(self) -> int:
        """Return the number of examples in the dataset."""
        return self._length

    def __getitem__(self, idx: int) -> Tuple[str, str, str]:
        """
        Retrieve a single example.

        Parameters
        ----------
        idx : int
            Index of the example.

        Returns
        -------
        Tuple[str, str, str]
            A tuple containing (prompt, chosen, rejected).
        """
        if idx < 0 or idx >= self._length:
            raise IndexError("Index out of range")
        entry = self._data[idx]
        return entry["prompt"], entry["chosen"], entry["rejected"]

    def __iter__(self) -> Iterator[Tuple[str, str, str]]:
        """Iterate over all examples in the dataset."""
        for entry in self._data:
            yield entry["prompt"], entry["chosen"], entry["rejected"]

    @property
    def data(self) -> List[Dict[str, Any]]:
        """Return the raw data list."""
        return self._data

    def get_batch(self, indices: List[int]) -> List[Tuple[str, str, str]]:
        """
        Retrieve a batch of examples given a list of indices.

        Parameters
        ----------
        indices : List[int]
            List of indices to fetch.

        Returns
        -------
        List[Tuple[str, str, str]]
            List of (prompt, chosen, rejected) tuples.
        """
        batch = []
        for idx in indices:
            batch.append(self[idx])
        return batch
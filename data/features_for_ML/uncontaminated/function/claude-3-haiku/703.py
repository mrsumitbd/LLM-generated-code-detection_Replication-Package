import os
import json
from typing import Tuple, Dict

def load_environment(
    dataset_name: str = "math",
    dataset_split: str = "train",
    num_train_examples: int = -1,
    max_turns: int = 100,
    **kwargs,
) -> Tuple[Dict, Dict]:
    """
    Loads the specified dataset and environment.

    Args:
        dataset_name (str): The name of the dataset to load. Defaults to "math".
        dataset_split (str): The split of the dataset to load. Defaults to "train".
        num_train_examples (int): The maximum number of training examples to load. Defaults to -1 (all).
        max_turns (int): The maximum number of turns in the environment. Defaults to 100.
        **kwargs: Additional keyword arguments to pass to the dataset and environment loaders.

    Returns:
        Tuple[Dict, Dict]: A tuple containing the dataset and the environment.
    """
    dataset_dir = os.path.join("data", dataset_name)
    dataset_path = os.path.join(dataset_dir, f"{dataset_split}.json")

    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    if num_train_examples > 0:
        dataset["examples"] = dataset["examples"][:num_train_examples]

    environment = {
        "max_turns": max_turns,
        **kwargs,
    }

    return dataset, environment
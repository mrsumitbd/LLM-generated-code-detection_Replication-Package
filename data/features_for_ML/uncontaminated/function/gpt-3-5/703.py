def load_environment(
    dataset_name: str = "math",
    dataset_split: str = "train",
    num_train_examples: int = -1,
    max_turns: int = 100,
    **kwargs,
):
    print(f"Loading environment for dataset: {dataset_name}, split: {dataset_split}, num_train_examples: {num_train_examples}, max_turns: {max_turns}")
    print("Additional keyword arguments:")
    for key, value in kwargs.items():
        print(f"{key}: {value}")
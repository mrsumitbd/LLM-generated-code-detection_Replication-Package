def print_metrics(metrics: dict[str, dict[str, float]]) -> None:
    """Print evaluation metrics in a readable format.

    :param metrics: A dictionary containing the evaluation metrics.
    :return: None
    """
    for category, values in metrics.items():
        print(f"\n{category}:")
        for key, value in values.items():
            print(f"  {key}: {value:.4f}")
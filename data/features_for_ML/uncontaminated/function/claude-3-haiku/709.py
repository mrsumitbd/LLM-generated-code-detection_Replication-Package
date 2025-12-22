def print_metrics(metrics: dict[str, dict[str, float]]) -> None:
    """Print evaluation metrics in a readable format.

    :param metrics: A dictionary containing the evaluation metrics.
    :return: None
    """
    for task, task_metrics in metrics.items():
        print(f"Task: {task}")
        for metric, value in task_metrics.items():
            print(f"  {metric}: {value:.4f}")
        print()
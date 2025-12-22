def print_metrics(metrics: dict[str, dict[str, float]]) -> None:
    """Print evaluation metrics in a readable format.

    :param metrics: A dictionary containing the evaluation metrics.
    :return: None
    """
    if not metrics:
        return

    for metric_name in sorted(metrics):
        submetrics = metrics[metric_name]
        print(f"{metric_name}:")
        if submetrics:
            for sub_name in sorted(submetrics):
                value = submetrics[sub_name]
                # Format floats to 4 decimal places, keep integers as is
                if isinstance(value, float):
                    formatted = f"{value:.4f}"
                else:
                    formatted = str(value)
                print(f"  {sub_name}: {formatted}")
        else:
            print("  (no submetrics)")
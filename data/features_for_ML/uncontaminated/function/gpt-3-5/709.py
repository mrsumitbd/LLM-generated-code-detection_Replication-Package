def print_metrics(metrics: dict[str, dict[str, float]]) -> None:
    for metric_name, metric_values in metrics.items():
        print(f"{metric_name}:")
        for key, value in metric_values.items():
            print(f"  {key}: {value}")
        print()
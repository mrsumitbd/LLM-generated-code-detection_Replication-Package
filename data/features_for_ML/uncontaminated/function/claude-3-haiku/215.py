def _compare_results_report(eval_set: str, left_side: CompareArgs, right_side: CompareArgs, output_format: str):
    from collections import defaultdict
    from typing import Dict, List, Tuple

    def _get_metric_values(compare_args: CompareArgs) -> Dict[str, float]:
        metric_values = defaultdict(float)
        for metric, value in compare_args.metrics.items():
            metric_values[metric] = value
        return metric_values

    def _format_report(metric_values: Dict[str, float], side: str) -> List[Tuple[str, float]]:
        report = []
        for metric, value in metric_values.items():
            report.append((f"{side}_{metric}", value))
        return report

    left_metric_values = _get_metric_values(left_side)
    right_metric_values = _get_metric_values(right_side)

    report = _format_report(left_metric_values, "left")
    report.extend(_format_report(right_metric_values, "right"))

    if output_format == "json":
        import json
        return json.dumps(dict(report), indent=2)
    elif output_format == "table":
        from tabulate import tabulate
        return tabulate(report, headers=["Metric", "Value"], tablefmt="grid")
    else:
        raise ValueError(f"Unsupported output format: {output_format}")
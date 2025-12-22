import json
import csv
import io
from typing import Any, Dict, List, Union

# Assuming CompareArgs is a simple container with `name` and `result` attributes.
# If it has a different structure, this function will still work as long as
# those attributes exist and `result` is a mapping or a scalar.
class CompareArgs:
    def __init__(self, name: str, result: Any):
        self.name = name
        self.result = result

def _compare_results_report(
    eval_set: str,
    left_side: CompareArgs,
    right_side: CompareArgs,
    output_format: str,
) -> str:
    """
    Generate a comparison report between two evaluation results.

    Parameters
    ----------
    eval_set : str
        Identifier for the evaluation set (used only in the report header).
    left_side : CompareArgs
        The left side of the comparison. Must have `name` and `result` attributes.
    right_side : CompareArgs
        The right side of the comparison. Must have `name` and `result` attributes.
    output_format : str
        One of 'text', 'json', or 'csv'. Determines the format of the returned report.

    Returns
    -------
    str
        The formatted comparison report.
    """
    # Helper to normalise results to a mapping
    def _to_dict(res: Any) -> Dict[str, Any]:
        if isinstance(res, dict):
            return res
        # If the result is a scalar, wrap it in a dict with a generic key
        return {"value": res}

    left_dict = _to_dict(left_side.result)
    right_dict = _to_dict(right_side.result)

    # Union of keys
    all_keys = sorted(set(left_dict.keys()) | set(right_dict.keys()))

    # Build rows
    rows: List[Dict[str, Union[str, Any]]] = []
    for key in all_keys:
        left_val = left_dict.get(key, None)
        right_val = right_dict.get(key, None)
        equal = left_val == right_val
        rows.append(
            {
                "key": key,
                "left_name": left_side.name,
                "left_value": left_val,
                "right_name": right_side.name,
                "right_value": right_val,
                "equal": equal,
            }
        )

    # Format output
    if output_format.lower() == "text":
        lines = [f"Comparison Report for '{eval_set}'"]
        lines.append(f"{'Key':<20} | {left_side.name:<15} | {right_side.name:<15} | Equal")
        lines.append("-" * 70)
        for r in rows:
            left_val_str = json.dumps(r["left_value"], ensure_ascii=False)
            right_val_str = json.dumps(r["right_value"], ensure_ascii=False)
            lines.append(
                f"{r['key']:<20} | {left_val_str:<15} | {right_val_str:<15} | {r['equal']}"
            )
        return "\n".join(lines)

    elif output_format.lower() == "json":
        # Convert rows to JSON serialisable form
        serialisable_rows = [
            {
                "key": r["key"],
                "left": {r["left_name"]: r["left_value"]},
                "right": {r["right_name"]: r["right_value"]},
                "equal": r["equal"],
            }
            for r in rows
        ]
        report = {
            "eval_set": eval_set,
            "comparison": serialisable_rows,
        }
        return json.dumps(report, indent=2, ensure_ascii=False)

    elif output_format.lower() == "csv":
        output = io.StringIO()
        fieldnames = [
            "key",
            f"{left_side.name}_value",
            f"{right_side.name}_value",
            "equal",
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {
                    "key": r["key"],
                    f"{left_side.name}_value": r["left_value"],
                    f"{right_side.name}_value": r["right_value"],
                    "equal": r["equal"],
                }
            )
        return output.getvalue()

    else:
        raise ValueError(
            f"Unsupported output_format '{output_format}'. "
            "Supported formats: 'text', 'json', 'csv'."
        )
import json
import os
import statistics
from typing import Any, Dict, List, Union

def generate_maestro_analysis_report(json_path: str) -> str:
    """
    Generate a simple analysis report for a JSON file.

    The report is written to a file named `maestro_analysis_report.txt` in the same
    directory as the input JSON file. The report contains:
        - Number of top‑level records (if the JSON is a list) or 1 (if a dict).
        - List of top‑level keys (if a dict).
        - For each numeric key, the count, mean, min, and max of the values.

    Parameters
    ----------
    json_path : str
        Path to the JSON file to analyze.

    Returns
    -------
    str
        Path to the generated report file.
    """
    # Load the JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Prepare report content
    report_lines: List[str] = []

    # Basic info
    if isinstance(data, list):
        report_lines.append(f"Top‑level type: list")
        report_lines.append(f"Number of records: {len(data)}")
        # If list of dicts, gather keys from first element
        if data and isinstance(data[0], dict):
            keys = set()
            for item in data:
                if isinstance(item, dict):
                    keys.update(item.keys())
            report_lines.append(f"Keys found in records: {sorted(keys)}")
    elif isinstance(data, dict):
        report_lines.append(f"Top‑level type: dict")
        report_lines.append(f"Number of keys: {len(data)}")
        report_lines.append(f"Keys: {sorted(data.keys())}")
    else:
        report_lines.append(f"Top‑level type: {type(data).__name__}")
        report_lines.append(f"Value: {data}")

    # Numeric analysis
    numeric_keys: Dict[str, List[Union[int, float]]] = {}
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (int, float)):
                numeric_keys.setdefault(k, []).append(v)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for k, v in item.items():
                    if isinstance(v, (int, float)):
                        numeric_keys.setdefault(k, []).append(v)

    if numeric_keys:
        report_lines.append("\nNumeric key statistics:")
        for k, values in numeric_keys.items():
            count = len(values)
            mean_val = statistics.mean(values)
            min_val = min(values)
            max_val = max(values)
            report_lines.append(
                f"  {k}: count={count}, mean={mean_val:.4f}, min={min_val}, max={max_val}"
            )
    else:
        report_lines.append("\nNo numeric keys found.")

    # Write report to file
    report_dir = os.path.dirname(os.path.abspath(json_path))
    report_path = os.path.join(report_dir, "maestro_analysis_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    return report_path
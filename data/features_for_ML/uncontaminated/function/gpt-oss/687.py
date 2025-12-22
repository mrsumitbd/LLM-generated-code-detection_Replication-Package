import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Union


def load_data(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Load data from various sources specified in a dictionary.

    The dictionary may contain one of the following keys:

    - ``data``: a pre‑existing dictionary to return directly.
    - ``json_str``: a JSON string to parse.
    - ``csv_str``: a CSV string to parse (comma separated by default).
    - ``file_path``: a path to a file to read.
      The ``format`` key must be provided and can be ``json`` or ``csv``.
      Optional ``delimiter`` and ``encoding`` keys are accepted for CSV.

    The function returns a dictionary. For CSV data the dictionary will
    contain a single key ``rows`` whose value is a list of row dictionaries.
    For JSON data the dictionary will contain a single key ``data`` whose
    value is the parsed JSON object.

    Parameters
    ----------
    data : dict
        Dictionary containing the source specification.

    Returns
    -------
    dict
        Loaded data in a dictionary form.
    """
    # 1. Direct data
    if "data" in data:
        return data["data"]

    # 2. JSON string
    if "json_str" in data:
        try:
            parsed = json.loads(data["json_str"])
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON string") from exc
        return {"data": parsed}

    # 3. CSV string
    if "csv_str" in data:
        delimiter = data.get("delimiter", ",")
        rows: List[Dict[str, str]] = []
        reader = csv.DictReader(data["csv_str"].splitlines(), delimiter=delimiter)
        for row in reader:
            rows.append(row)
        return {"rows": rows}

    # 4. File based loading
    if "file_path" in data:
        file_path = Path(data["file_path"])
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        fmt = data.get("format", "").lower()
        if fmt == "json":
            with file_path.open("r", encoding=data.get("encoding", "utf-8")) as f:
                try:
                    parsed = json.load(f)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON file: {file_path}") from exc
            return {"data": parsed}

        if fmt == "csv":
            delimiter = data.get("delimiter", ",")
            rows: List[Dict[str, str]] = []
            with file_path.open("r", encoding=data.get("encoding", "utf-8")) as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                for row in reader:
                    rows.append(row)
            return {"rows": rows}

        raise ValueError(f"Unsupported format '{fmt}'. Supported formats: json, csv")

    # 5. Nothing found
    raise ValueError("No valid data source specified in the input dictionary.")
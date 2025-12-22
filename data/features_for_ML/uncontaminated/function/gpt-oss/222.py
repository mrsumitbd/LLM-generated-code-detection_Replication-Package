import json
import os
from typing import Dict, Any


def convert_txt_to_json(txt_filepath: str, json_filepath: str, method: str, model: str, directory_path: str) -> None:
    """
    Convert analysis results from txt format to structured JSON format.

    Args:
        txt_filepath: Path to the input txt file
        json_filepath: Path to the output json file
        method: Analysis method used
        model: Model used for analysis
        directory_path: Input directory path
    """
    # Read the entire text file
    try:
        with open(txt_filepath, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except Exception as e:
        raise RuntimeError(f"Failed to read txt file '{txt_filepath}': {e}")

    # Helper to parse a line into key/value
    def _parse_line(line: str) -> Any:
        # Try common separators
        for sep in [":", "=", "->"]:
            if sep in line:
                key, val = line.split(sep, 1)
                return key.strip(), val.strip()
        # If no separator, treat whole line as a message
        return None, line.strip()

    # Build a dictionary from the lines
    results: Dict[str, Any] = {}
    for line in lines:
        if not line.strip():
            continue
        key, val = _parse_line(line)
        if key is None:
            # Append to a generic messages list
            results.setdefault("messages", []).append(val)
        else:
            # If key already exists, convert to list
            if key in results:
                if isinstance(results[key], list):
                    results[key].append(val)
                else:
                    results[key] = [results[key], val]
            else:
                results[key] = val

    # Add metadata
    metadata = {
        "method": method,
        "model": model,
        "directory_path": directory_path,
        "source_file": os.path.basename(txt_filepath),
    }

    output = {
        "metadata": metadata,
        "results": results,
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(json_filepath), exist_ok=True)

    # Write JSON
    try:
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise RuntimeError(f"Failed to write json file '{json_filepath}': {e}")
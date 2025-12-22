import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

def export_traces_json(
    traces: List[Any],
    output_path: Union[str, Path],
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Export traces to JSON format with metadata.

    Args:
        traces: List of trace objects with to_dict() method.
        output_path: Path to save the JSON file.
        metadata: Optional metadata to include in the output.
    """
    # Ensure output_path is a Path object
    out_path = Path(output_path)

    # Create parent directories if they don't exist
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert traces to dictionaries
    trace_dicts = [trace.to_dict() for trace in traces]

    # Build the final payload
    payload: Dict[str, Any] = {"traces": trace_dicts}
    if metadata is not None:
        payload["metadata"] = metadata

    # Write JSON to file
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

def export_traces_json(traces: List[Any], output_path: Union[str, Path], metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Export traces to JSON format with metadata
    
    Args:
        traces: List of trace objects with to_dict() method
        output_path: Path to save the JSON file
        metadata: Optional metadata to include in the output
    """
    data = {
        "traces": [trace.to_dict() for trace in traces],
        "metadata": metadata or {}
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        json.dump(data, f, indent=2)
import json
import time
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
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert traces to dictionaries
    trace_dicts = []
    for trace in traces:
        if hasattr(trace, 'to_dict'):
            trace_dicts.append(trace.to_dict())
        else:
            trace_dicts.append(trace)
    
    # Build output structure
    output_data = {
        "metadata": metadata or {},
        "traces": trace_dicts
    }
    
    # Add default metadata
    output_data["metadata"].setdefault("total_traces", len(trace_dicts))
    output_data["metadata"].setdefault("exported_at", time.time())
    
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    logger.info(f"Exported {len(traces)} traces to {output_path}")
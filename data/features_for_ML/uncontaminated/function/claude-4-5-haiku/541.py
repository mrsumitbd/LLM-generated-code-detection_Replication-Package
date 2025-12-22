def export_traces_json(traces: List[Any], output_path: Union[str, Path], metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Export traces to JSON format with metadata
    
    Args:
        traces: List of trace objects with to_dict() method
        output_path: Path to save the JSON file
        metadata: Optional metadata to include in the output
    """
    import json
    from pathlib import Path
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    traces_data = []
    for trace in traces:
        if hasattr(trace, 'to_dict'):
            traces_data.append(trace.to_dict())
        else:
            traces_data.append(trace)
    
    output = {
        'traces': traces_data
    }
    
    if metadata is not None:
        output['metadata'] = metadata
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
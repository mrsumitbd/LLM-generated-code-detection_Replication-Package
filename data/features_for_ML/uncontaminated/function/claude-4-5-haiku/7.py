def generate_maestro_analysis_report(json_path: str):
    import json
    import os
    from pathlib import Path
    
    # Load the JSON file
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract relevant information from the JSON
    report = {
        "title": "Maestro Analysis Report",
        "data": data,
        "summary": {}
    }
    
    # Generate summary statistics if data is a list
    if isinstance(data, list):
        report["summary"]["total_items"] = len(data)
        report["summary"]["items"] = data
    elif isinstance(data, dict):
        report["summary"]["keys"] = list(data.keys())
        report["summary"]["data"] = data
    
    return report
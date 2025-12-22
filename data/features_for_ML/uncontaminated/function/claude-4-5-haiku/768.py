def run_analysis():
    import os
    import json
    from pathlib import Path
    
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Define paths for data files
    data_dir = script_dir / "data"
    results_dir = script_dir / "results"
    
    # Create results directory if it doesn't exist
    results_dir.mkdir(exist_ok=True)
    
    # Initialize results dictionary
    results = {
        "status": "completed",
        "timestamp": None,
        "data_files": [],
        "analysis_results": {}
    }
    
    # Get current timestamp
    from datetime import datetime
    results["timestamp"] = datetime.now().isoformat()
    
    # Check if data directory exists
    if not data_dir.exists():
        results["status"] = "error"
        results["error"] = "Data directory not found"
        return results
    
    # Process all JSON files in data directory
    for file_path in data_dir.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            results["data_files"].append(file_path.name)
            
            # Perform basic analysis
            if isinstance(data, list):
                results["analysis_results"][file_path.name] = {
                    "type": "list",
                    "count": len(data),
                    "sample": data[0] if data else None
                }
            elif isinstance(data, dict):
                results["analysis_results"][file_path.name] = {
                    "type": "dict",
                    "keys": list(data.keys()),
                    "size": len(data)
                }
            else:
                results["analysis_results"][file_path.name] = {
                    "type": type(data).__name__,
                    "value": str(data)
                }
        
        except Exception as e:
            results["analysis_results"][file_path.name] = {
                "error": str(e)
            }
    
    # Save results to file
    results_file = results_dir / "analysis_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return results
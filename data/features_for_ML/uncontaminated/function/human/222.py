import json
import datetime

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
    try:
        with open(txt_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the content to extract structured information
        lines = content.split('\n')
        
        # Initialize the JSON structure
        result = {
            "metadata": {
                "method": method,
                "model": model,
                "input_directory": directory_path,
                "timestamp": datetime.datetime.now().isoformat(),
                "analysis_type": "failure_attribution"
            },
            "files_analyzed": [],
            "summary": {
                "total_files": 0,
                "files_with_errors": 0,
                "files_without_errors": 0
            }
        }
        
        current_file = None
        current_file_data = None
        collecting_reason = False
        reason_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Detect file processing start
            if line.startswith("=== File:") and line.endswith("==="):
                # Save previous file if exists
                if current_file_data:
                    # Finalize reason collection if needed
                    if collecting_reason and reason_lines:
                        current_file_data["analysis_result"]["error_reason"] = " ".join(reason_lines).strip()
                        current_file_data["analysis_result"]["error_detected"] = True
                    result["files_analyzed"].append(current_file_data)
                
                # Start new file
                filename = line.replace("=== File:", "").replace("===", "").strip()
                current_file_data = {
                    "filename": filename,
                    "analysis_result": {
                        "error_detected": False,
                        "error_agent": None,
                        "error_step": None,
                        "error_type": None,
                        "error_reason": None
                    }
                }
                current_file = filename
                collecting_reason = False
                reason_lines = []
            
            # Collect analysis content for current file
            elif current_file_data and line and not line.startswith("==="):
                
                # Parse specific error information for all_at_once method
                if line.startswith("Error Agent:"):
                    collecting_reason = False
                    error_agent = line.replace("Error Agent:", "").strip()
                    if error_agent.lower() not in ["no error", "none", ""]:
                        current_file_data["analysis_result"]["error_detected"] = True
                        current_file_data["analysis_result"]["error_agent"] = error_agent
                
                elif line.startswith("Error Step:"):
                    collecting_reason = False
                    error_step = line.replace("Error Step:", "").strip()
                    if error_step.lower() not in ["no error", "none", ""]:
                        try:
                            current_file_data["analysis_result"]["error_step"] = int(error_step)
                        except ValueError:
                            current_file_data["analysis_result"]["error_step"] = error_step
                
                elif line.startswith("Error Type:"):
                    collecting_reason = False
                    error_type = line.replace("Error Type:", "").strip()
                    if error_type.lower() not in ["no error", "none", ""]:
                        current_file_data["analysis_result"]["error_type"] = error_type
                        # If we have error_type, it means error is detected
                        current_file_data["analysis_result"]["error_detected"] = True
                
                elif line.startswith("Reason:") or line.startswith("Error Description:"):
                    reason = line.replace("Reason:", "").replace("Error Description:", "").strip()
                    if reason.lower() not in ["no error", "none", ""]:
                        current_file_data["analysis_result"]["error_reason"] = reason
                        # If we have error_reason, it means error is detected
                        current_file_data["analysis_result"]["error_detected"] = True
                        collecting_reason = False
                    else:
                        # Start collecting multi-line reason content
                        collecting_reason = True
                        reason_lines = []
                
                # Parse step_by_step method output format: "Error detected at Step X by Agent Y"
                elif "Error detected at Step" in line and "by Agent" in line:
                    collecting_reason = False
                    current_file_data["analysis_result"]["error_detected"] = True
                    # Extract step number and agent
                    try:
                        step_part = line.split("Step")[1].split("by")[0].strip()
                        current_file_data["analysis_result"]["error_step"] = int(step_part)
                        agent_part = line.split("by Agent")[1].strip()
                        current_file_data["analysis_result"]["error_agent"] = agent_part
                    except (IndexError, ValueError):
                        pass
                
                elif "Error found at Step" in line:
                    collecting_reason = False
                    current_file_data["analysis_result"]["error_detected"] = True
                    # Extract step number
                    try:
                        step_part = line.split("Step")[1].split("by")[0].strip()
                        current_file_data["analysis_result"]["error_step"] = int(step_part)
                    except (IndexError, ValueError):
                        pass
                
                elif "No errors detected" in line or "No Error" in line:
                    collecting_reason = False
                    current_file_data["analysis_result"]["error_detected"] = False
                
                # Collect multi-line reason content
                elif collecting_reason and line and not line.startswith("**"):
                    reason_lines.append(line)
            
            # Handle empty lines or lines starting with ** when collecting reason
            elif current_file_data and collecting_reason and (not line or line.startswith("**")):
                continue
        
        # Add the last file if exists
        if current_file_data:
            # Finalize reason collection if needed for the last file
            if collecting_reason and reason_lines:
                current_file_data["analysis_result"]["error_reason"] = " ".join(reason_lines).strip()
                current_file_data["analysis_result"]["error_detected"] = True
            result["files_analyzed"].append(current_file_data)
        
        # Calculate summary statistics
        result["summary"]["total_files"] = len(result["files_analyzed"])
        result["summary"]["files_with_errors"] = sum(1 for f in result["files_analyzed"] 
                                                      if f["analysis_result"]["error_detected"])
        result["summary"]["files_without_errors"] = (result["summary"]["total_files"] - 
                                                      result["summary"]["files_with_errors"])
        
        # Write JSON file
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"JSON output saved to: {json_filepath}")
        
    except Exception as e:
        print(f"Error converting to JSON: {e}")
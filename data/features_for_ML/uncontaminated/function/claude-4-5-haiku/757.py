def run_simulation_hpc(script_path: str) -> RunOut:
    import subprocess
    import json
    import os
    from pathlib import Path
    
    # Validate script path exists
    if not os.path.exists(script_path):
        return RunOut(
            success=False,
            stdout="",
            stderr=f"Script not found: {script_path}",
            return_code=1
        )
    
    try:
        # Run the script using subprocess
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            timeout=3600
        )
        
        return RunOut(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode
        )
    
    except subprocess.TimeoutExpired:
        return RunOut(
            success=False,
            stdout="",
            stderr="Script execution timed out after 3600 seconds",
            return_code=-1
        )
    
    except Exception as e:
        return RunOut(
            success=False,
            stdout="",
            stderr=f"Error executing script: {str(e)}",
            return_code=-1
        )
def add_cron_job(server_name, base_dir, script_direct):
    """Adds a new cron job for the specified server.

    Args:
        server_name (str): The name of the server.
        base_dir (str): Base directory.
        script_dir (str): Script directory.

    Returns:
        int: 0 on success, error code on failure.
    """
    import subprocess
    import os
    
    try:
        # Validate inputs
        if not server_name or not base_dir or not script_direct:
            return 1
        
        # Check if script directory exists
        if not os.path.isdir(script_direct):
            return 2
        
        # Check if base directory exists
        if not os.path.isdir(base_dir):
            return 3
        
        # Create cron job command
        script_path = os.path.join(script_direct, f"{server_name}.sh")
        
        # Check if script exists
        if not os.path.isfile(script_path):
            return 4
        
        # Get current crontab
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True,
                timeout=5
            )
            current_crontab = result.stdout if result.returncode == 0 else ""
        except Exception:
            current_crontab = ""
        
        # Create new cron job entry (daily at 2 AM)
        cron_entry = f"0 2 * * * {script_path}\n"
        
        # Check if job already exists
        if cron_entry.strip() in current_crontab:
            return 5
        
        # Add new cron job
        new_crontab = current_crontab + cron_entry
        
        # Write new crontab
        process = subprocess.Popen(
            ["crontab", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=new_crontab, timeout=5)
        
        if process.returncode != 0:
            return 6
        
        return 0
        
    except subprocess.TimeoutExpired:
        return 7
    except Exception as e:
        return 8
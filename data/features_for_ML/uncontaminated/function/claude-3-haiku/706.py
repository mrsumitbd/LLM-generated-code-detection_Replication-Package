import os
import subprocess

def add_cron_job(server_name, base_dir, script_dir):
    """Adds a new cron job for the specified server.

    Args:
        server_name (str): The name of the server.
        base_dir (str): Base directory.
        script_dir (str): Script directory.

    Returns:
        int: 0 on success, error code on failure.
    """
    try:
        script_path = os.path.join(base_dir, script_dir)
        cron_job = f"0 0 * * * {script_path}/script.py"
        subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["crontab", "-"], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error adding cron job for {server_name}: {e}")
        return 1
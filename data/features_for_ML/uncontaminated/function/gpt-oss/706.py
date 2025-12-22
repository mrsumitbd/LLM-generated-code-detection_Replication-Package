import os
import subprocess
from typing import List


def _read_current_crontab() -> List[str]:
    """Return the current crontab lines as a list."""
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.splitlines()
        # If no crontab exists, treat as empty
        if result.returncode == 1:
            return []
        # Other errors
        raise RuntimeError(f"crontab -l failed: {result.stderr}")
    except Exception as exc:
        raise RuntimeError(f"Failed to read crontab: {exc}") from exc


def _write_crontab(lines: List[str]) -> None:
    """Write the given lines to the crontab."""
    data = "\n".join(lines) + ("\n" if lines else "")
    try:
        subprocess.run(
            ["crontab", "-"],
            input=data,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Failed to write crontab: {exc}") from exc


def add_cron_job(server_name: str, base_dir: str, script_dir: str) -> int:
    """
    Adds a new cron job for the specified server.

    Args:
        server_name (str): The name of the server.
        base_dir (str): Base directory.
        script_dir (str): Script directory.

    Returns:
        int: 0 on success, error code on failure.
    """
    # Resolve the script path
    script_path = os.path.join(base_dir, script_dir)
    if not os.path.isfile(script_path):
        # Script does not exist
        return 1

    # Build the cron line (run daily at midnight)
    log_path = os.path.join(base_dir, f"{server_name}.log")
    cron_line = (
        f"0 0 * * * {script_path} >> {log_path} 2>&1 # cron job for {server_name}"
    )

    try:
        current_lines = _read_current_crontab()
    except RuntimeError:
        return 2

    # Avoid duplicate entries
    if any(cron_line in line for line in current_lines):
        return 0  # Already present

    current_lines.append(cron_line)

    try:
        _write_crontab(current_lines)
    except RuntimeError:
        return 3

    return 0
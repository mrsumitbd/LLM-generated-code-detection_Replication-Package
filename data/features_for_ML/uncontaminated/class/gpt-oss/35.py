import os
import re
import datetime
from pathlib import Path
from typing import Optional


class GetLog:
    @classmethod
    def get_log(
        cls,
        log_level: str = "info",
        save_locally: bool = False,
        shared_log_folder: Optional[str] = None,
    ) -> str:
        """
        Retrieve log entries from a log file, optionally filtering by log level
        and optionally saving the retrieved logs locally.

        Parameters
        ----------
        log_level : str, optional
            The log level to filter by (e.g., "info", "warning", "error").
            Case-insensitive. Defaults to "info".
        save_locally : bool, optional
            If True, the retrieved logs are written to a local file named
            `log_<timestamp>.txt`. Defaults to False.
        shared_log_folder : str, optional
            Path to a folder containing the log file. If None, the current
            working directory is used. The method looks for a file named
            `app.log` in the specified folder.

        Returns
        -------
        str
            The concatenated log entries that match the specified level.
        """
        # Determine the log file path
        log_dir = Path(shared_log_folder) if shared_log_folder else Path.cwd()
        log_file = log_dir / "app.log"

        # If the log file does not exist, return an empty string
        if not log_file.is_file():
            return ""

        # Read the log file
        try:
            with log_file.open("r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            return ""

        # Compile a regex pattern for the log level (case-insensitive)
        level_pattern = re.compile(rf"\b{re.escape(log_level)}\b", re.IGNORECASE)

        # Filter lines that contain the log level
        filtered_lines = [line for line in lines if level_pattern.search(line)]

        # Join the filtered lines into a single string
        log_content = "".join(filtered_lines)

        # Optionally save the logs locally
        if save_locally and log_content:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            local_file = Path.cwd() / f"log_{timestamp}.txt"
            try:
                with local_file.open("w", encoding="utf-8") as f:
                    f.write(log_content)
            except Exception:
                # If saving fails, ignore and continue
                pass

        return log_content
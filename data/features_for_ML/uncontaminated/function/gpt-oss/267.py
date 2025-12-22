import os
import sys
from pathlib import Path
from typing import List

def site_config_dirs(appname: str) -> List[str]:
    """
    Return a list of directories that should be searched for site‑wide
    configuration files for the given application name.

    The order of the returned directories is from most specific to least
    specific, i.e. user‑specific directories first, then system‑wide ones.
    """
    dirs: List[Path] = []

    # Windows
    if sys.platform.startswith("win"):
        # User‑specific config
        appdata = os.getenv("APPDATA")
        if appdata:
            dirs.append(Path(appdata) / appname)

        # Local app data (often used for non‑roaming data)
        local_appdata = os.getenv("LOCALAPPDATA")
        if local_appdata:
            dirs.append(Path(local_appdata) / appname)

        # System‑wide config (common convention)
        program_data = os.getenv("PROGRAMDATA")
        if program_data:
            dirs.append(Path(program_data) / appname)

    # POSIX (Linux, macOS, etc.)
    else:
        # XDG config home
        xdg_config_home = os.getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            dirs.append(Path(xdg_config_home) / appname)
        else:
            # Default to ~/.config
            dirs.append(Path.home() / ".config" / appname)

        # System‑wide config directory
        # On Linux, /etc/<appname> is common; on macOS, /Library/Application Support/<appname>
        if sys.platform == "darwin":
            dirs.append(Path("/Library/Application Support") / appname)
        else:
            dirs.append(Path("/etc") / appname)

    # Convert to string paths and return
    return [str(p) for p in dirs]
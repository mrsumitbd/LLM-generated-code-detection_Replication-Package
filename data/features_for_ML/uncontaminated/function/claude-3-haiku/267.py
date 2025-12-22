import os
from typing import List

def site_config_dirs(appname: str) -> List[str]:
    """
    Returns a list of directories where the application's configuration files
    are expected to be found.

    Args:
        appname (str): The name of the application.

    Returns:
        List[str]: A list of directory paths where the application's configuration
        files are expected to be found.
    """
    config_dirs = []

    # Check the XDG Base Directory Specification
    xdg_config_home = os.getenv("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config"))
    config_dirs.append(os.path.join(xdg_config_home, appname))

    # Check the system-wide configuration directory
    if os.name == "posix":
        config_dirs.append(os.path.join("/etc", appname))

    # Check the current working directory
    config_dirs.append(os.path.join(os.getcwd(), "config"))

    return config_dirs
import os
import sys
from typing import List


def site_config_dirs(appname: str) -> List[str]:
    """
    Return a list of site configuration directories for the given application name.
    
    This follows platform conventions:
    - On Windows: uses PROGRAMDATA and ALLUSERSPROFILE
    - On macOS: uses /Library/Application Support
    - On Linux/Unix: uses /etc and /usr/local/etc
    """
    dirs = []
    
    if sys.platform == "win32":
        # Windows: use PROGRAMDATA and ALLUSERSPROFILE
        programdata = os.environ.get("PROGRAMDATA")
        if programdata:
            dirs.append(os.path.join(programdata, appname))
        
        allusersprofile = os.environ.get("ALLUSERSPROFILE")
        if allusersprofile:
            dirs.append(os.path.join(allusersprofile, appname))
    
    elif sys.platform == "darwin":
        # macOS: use /Library/Application Support
        dirs.append(os.path.join("/Library/Application Support", appname))
    
    else:
        # Linux/Unix: use /etc and /usr/local/etc
        dirs.append(os.path.join("/etc", appname))
        dirs.append(os.path.join("/usr/local/etc", appname))
    
    return dirs
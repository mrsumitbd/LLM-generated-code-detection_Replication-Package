from typing import NamedTuple

class SysValues(NamedTuple):
    executable: str
    version: str
    location: str

def get_pip_sys_values() -> SysValues:
    import sys
    import os

    executable = sys.executable
    version = sys.version.split()[0]
    location = os.path.dirname(executable)

    return SysValues(executable=executable, version=version, location=location)
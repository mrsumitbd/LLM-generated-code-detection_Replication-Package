import sys
from dataclasses import dataclass

@dataclass
class SysValues:
    python_version: str
    platform: str
    executable: str
    prefix: str
    base_prefix: str
    exec_prefix: str
    base_exec_prefix: str

def get_pip_sys_values() -> SysValues:
    """
    Returns various sys values as they are in the *target* environment.
    This is because pipask is typically installed in a different environment (e.g., pipx)
    than the installation target environment.
    """
    return SysValues(
        python_version=sys.version.split()[0],
        platform=sys.platform,
        executable=sys.executable,
        prefix=sys.prefix,
        base_prefix=sys.base_prefix,
        exec_prefix=sys.exec_prefix,
        base_exec_prefix=sys.base_exec_prefix
    )
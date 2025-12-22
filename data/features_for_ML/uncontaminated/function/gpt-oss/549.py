import platform
from typing import Any

# The PLATFORM type is expected to be a string representing the OS name
# (e.g., "Linux", "Windows", "Darwin").  If a different type is used,
# the function will still attempt to work with it by converting to a string.
PLATFORM = Any

def get_arch(system: PLATFORM) -> str:
    """
    Return a canonical architecture string for the given operating system.

    Parameters
    ----------
    system : PLATFORM
        The name of the operating system.  It is typically obtained from
        `platform.system()` but any string that represents the OS is accepted.

    Returns
    -------
    str
        A canonical architecture identifier such as 'x86_64', 'arm64',
        'i386', or the raw machine string if no mapping is found.
    """
    # Normalise the system name to a string
    sys_name = str(system).strip().lower()

    # Determine the machine architecture
    machine = platform.machine().lower()

    # Canonical mapping for common architectures
    arch_map = {
        # 64‑bit x86
        'x86_64': 'x86_64',
        'amd64': 'x86_64',
        # 32‑bit x86
        'i386': 'i386',
        'i486': 'i386',
        'i586': 'i386',
        'i686': 'i386',
        # ARM 64‑bit
        'arm64': 'arm64',
        'aarch64': 'arm64',
        # ARM 32‑bit
        'armv7l': 'armv7l',
        'armv6l': 'armv6l',
        # PowerPC
        'ppc64le': 'ppc64le',
        'ppc64': 'ppc64',
        'ppc': 'ppc',
    }

    # If the machine string is in the mapping, return the canonical form
    if machine in arch_map:
        return arch_map[machine]

    # Some OSes expose a different machine string; try to infer from OS
    if sys_name in ('windows', 'win32'):
        # Windows typically reports 'AMD64' for 64‑bit
        if machine in ('amd64', 'x86_64'):
            return 'x86_64'
        if machine in ('i386', 'i686'):
            return 'i386'
    elif sys_name in ('linux', 'darwin', 'macos'):
        # On Linux and macOS the machine string is usually accurate
        return machine

    # Fallback: return the raw machine string
    return machine
import subprocess
from ipaddress import (
    IPv4Network,
    IPv6Network,
    IPv4Address,
    IPv6Address,
)
from typing import List, Union


def _get_ssh_hostkeys(
    host: Union[str, IPv4Network, IPv6Network, IPv4Address, IPv6Address],
    port: int,
) -> List[str]:
    """
    Retrieve SSH host keys for the given host or network.

    Parameters
    ----------
    host : str | IPv4Network | IPv6Network | IPv4Address | IPv6Address
        The target host or network. If a network is supplied, host keys are
        retrieved for every address in the network.
    port : int
        The SSH port to query.

    Returns
    -------
    List[str]
        A list of host key lines returned by ssh-keyscan. Empty lines are
        omitted. If a network is supplied, the list contains keys for all
        hosts in the network in the order they are iterated.
    """
    # Helper to run ssh-keyscan for a single address
    def _scan(addr: str) -> List[str]:
        try:
            result = subprocess.run(
                ["ssh-keyscan", "-p", str(port), addr],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                # ssh-keyscan returns non-zero if it cannot connect
                return []
            # Split into lines, strip whitespace, filter out empty lines
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
        except (subprocess.SubprocessError, OSError):
            return []

    # Resolve host to a list of address strings
    if isinstance(host, (IPv4Address, IPv6Address)):
        addresses = [str(host)]
    elif isinstance(host, (IPv4Network, IPv6Network)):
        addresses = [str(addr) for addr in host.hosts()]
    else:
        # Assume string; could be hostname or IP
        addresses = [host]

    # Collect keys for each address
    keys: List[str] = []
    for addr in addresses:
        keys.extend(_scan(addr))

    return keys
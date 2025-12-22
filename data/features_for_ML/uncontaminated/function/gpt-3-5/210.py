from ipaddress import IPv4Network, IPv6Network, IPv4Address, IPv6Address

def _get_ssh_hostkeys(host: (str, IPv4Network, IPv6Network, IPv4Address, IPv6Address), port: int) -> list[str]:
    hostkeys = []
    # Implement your logic here to get SSH hostkeys for the given host and port
    return hostkeys
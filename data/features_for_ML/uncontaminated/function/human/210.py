from ipaddress import IPv4Network, IPv6Network, IPv4Address, IPv6Address, ip_address
from aw.utils.debug import log
from aw.utils.subps import process

def _get_ssh_hostkeys(host: (str, IPv4Network, IPv6Network, IPv4Address, IPv6Address), port: int) -> list[str]:
    result = process(
        cmd=f'ssh-keyscan -p{port} -T 2 -H {host}',
        timeout_sec=5,
    )

    if result['rc'] != 0:
        log(msg=f"SSH-hostkey target is unreachable: {host} -p {port}", level=5)
        return []

    data = []
    for line in result['stdout'].split('\n'):
        if line.startswith('|'):
            data.append(line.strip())

    return data
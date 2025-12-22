import socket
import paramiko

def _get_ssh_hostkeys(host: (str, 'IPv4Network', 'IPv6Network', 'IPv4Address', 'IPv6Address'), port: int) -> list[str]:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((str(host), port))
        transport = paramiko.Transport(sock)
        transport.start_client()
        host_keys = transport.get_remote_server_key()
        return [str(host_keys)]
    except (socket.error, paramiko.SSHException):
        return []
    finally:
        try:
            transport.close()
            sock.close()
        except (AttributeError, socket.error):
            pass
import socket
import paramiko
from ipaddress import IPv4Network, IPv6Network, IPv4Address, IPv6Address

def _get_ssh_hostkeys(host: (str, IPv4Network, IPv6Network, IPv4Address, IPv6Address), port: int) -> list[str]:
    """
    Get SSH host keys from a remote host.
    
    Args:
        host: The hostname or IP address (can be str, IPv4Network, IPv6Network, IPv4Address, or IPv6Address)
        port: The SSH port number
        
    Returns:
        A list of SSH host keys in string format
    """
    # Convert host to string if it's an IP address object
    if isinstance(host, (IPv4Network, IPv6Network, IPv4Address, IPv6Address)):
        host_str = str(host)
    else:
        host_str = host
    
    hostkeys = []
    
    try:
        # Create a socket connection to get the host key
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host_str, port))
        
        # Use paramiko's transport to get the host key
        transport = paramiko.Transport(sock)
        transport.start_client()
        
        # Get the remote server key
        remote_server_key = transport.get_remote_server_key()
        
        if remote_server_key:
            # Convert the key to different formats
            key_type = remote_server_key.get_name()
            key_blob = remote_server_key.asbytes()
            
            # Create the host key string in OpenSSH format
            import base64
            key_str = f"{key_type} {base64.b64encode(key_blob).decode('ascii')}"
            hostkeys.append(key_str)
        
        transport.close()
        sock.close()
        
    except Exception as e:
        # If paramiko approach fails, try using ssh-keyscan if available
        import subprocess
        try:
            result = subprocess.run(
                ['ssh-keyscan', '-p', str(port), host_str],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.stdout:
                # Parse the output from ssh-keyscan
                for line in result.stdout.strip().split('\n'):
                    if line and not line.startswith('#'):
                        # Extract just the key part (remove host:port prefix)
                        parts = line.split(' ', 2)
                        if len(parts) >= 3:
                            hostkeys.append(f"{parts[1]} {parts[2]}")
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass
    
    return hostkeys
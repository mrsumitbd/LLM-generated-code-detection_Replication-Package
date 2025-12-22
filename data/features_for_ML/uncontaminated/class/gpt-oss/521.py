import socket
from typing import Optional


class DashboardSpec:
    """
    A simple specification holder for a dashboard service.
    It can optionally be initialized with a specific IP address.
    If no IP is provided, the instance will attempt to determine the
    machine's non‑loopback IPv4 address.
    """

    def __init__(self, ip: Optional[str] = None) -> None:
        """
        Initialize the DashboardSpec.

        :param ip: Optional explicit IP address to use.
        """
        self._ip = ip

    def get_ip(self) -> str:
        """
        Return the IP address for the dashboard.

        If an explicit IP was supplied during initialization, that value
        is returned. Otherwise, the method attempts to discover the
        machine's first non‑loopback IPv4 address. If discovery fails,
        it falls back to the loopback address '127.0.0.1'.

        :return: A string representation of an IPv4 address.
        """
        if self._ip:
            return self._ip

        # Attempt to resolve the hostname to an IP address.
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if ip.startswith("127."):
                # If the resolved IP is loopback, try a socket trick
                # to get the outward facing IP.
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    try:
                        # The address doesn't need to be reachable.
                        s.connect(("8.8.8.8", 80))
                        ip = s.getsockname()[0]
                    except Exception:
                        # If the trick fails, keep the loopback IP.
                        pass
            return ip
        except Exception:
            # Fallback to loopback if anything goes wrong.
            return "127.0.0.1"
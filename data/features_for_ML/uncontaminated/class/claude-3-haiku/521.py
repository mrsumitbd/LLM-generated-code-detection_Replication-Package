class DashboardSpec:
    def __init__(self, ip_address: str):
        self._ip_address = ip_address

    def get_ip(self) -> str:
        return self._ip_address
class DashboardSpec:

    def __init__(self, ip: str = ""):
        self._ip = ip

    def get_ip(self) -> str:
        return self._ip
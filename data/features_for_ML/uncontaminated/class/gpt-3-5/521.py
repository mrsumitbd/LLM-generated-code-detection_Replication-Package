class DashboardSpec:
    
    def __init__(self, ip: str):
        self.ip = ip

    def get_ip(self) -> str:
        return self.ip
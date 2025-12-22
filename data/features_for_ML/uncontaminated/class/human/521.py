
class DashboardSpec:
    port: int = 8080

    def get_ip(self) -> str:
        return f"http://127.0.0.1:{self.port}"
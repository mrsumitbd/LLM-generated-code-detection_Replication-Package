class ProbeResult:

    def __init__(self) -> None:
        self.success = False
        self.error = None
        self.data = None
        self.latency = 0.0
        self.timestamp = None
        self.retries = 0
        self.status_code = None
        self.response_time = None
        self.message = ""
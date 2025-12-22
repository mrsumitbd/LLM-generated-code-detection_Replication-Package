class ProbeResult:
    def __init__(self) -> None:
        self.status = None
        self.response_time = None
        self.error_message = None

    def set_status(self, status: str) -> None:
        self.status = status

    def set_response_time(self, response_time: float) -> None:
        self.response_time = response_time

    def set_error_message(self, error_message: str) -> None:
        self.error_message = error_message

    def get_status(self) -> str:
        return self.status

    def get_response_time(self) -> float:
        return self.response_time

    def get_error_message(self) -> str:
        return self.error_message
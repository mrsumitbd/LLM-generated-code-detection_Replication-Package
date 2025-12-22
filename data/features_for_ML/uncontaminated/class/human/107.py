
class ProbeResult:
    def __init__(self) -> None:
        self.is_success = False
        self.config_data = {}
        self.probing_messages = []
        self.data = None

    is_success: bool
    config_data: dict
    probing_messages: list[str]
    data: ProbeData | None = None
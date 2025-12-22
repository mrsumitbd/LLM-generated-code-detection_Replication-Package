class SMState:
    """State machine state container."""

    def __init__(self):
        self.state = None
        self.data = {}

    def reset(self) -> None:
        self.state = None
        self.data = {}

    def set_state(self, state: str) -> None:
        self.state = state

    def get_state(self) -> str:
        return self.state

    def set_data(self, key: str, value) -> None:
        self.data[key] = value

    def get_data(self, key: str):
        return self.data.get(key, None)
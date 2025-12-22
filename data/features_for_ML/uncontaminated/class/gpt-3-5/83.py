class SMState:
    """State machine state container."""

    def __init__(self):
        self.state = None

    def reset(self) -> None:
        self.state = None
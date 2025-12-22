class ChatNoop:
    """A test model that returns an empty response."""

    def __init__(self):
        pass

    def invoke(self, messages):
        return []

    def stream(self, messages):
        for _ in messages:
            yield []
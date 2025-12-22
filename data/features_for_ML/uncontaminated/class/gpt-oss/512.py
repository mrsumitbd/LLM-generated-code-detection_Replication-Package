class ChatNoop:
    """A test model that returns an empty response."""

    def __init__(self):
        pass

    def invoke(self, messages):
        """Return an empty string as the model response."""
        return ""

    def stream(self, messages):
        """Yield nothing, simulating an empty streaming response."""
        return
        yield  # This line is never reached, but keeps the function a generator.
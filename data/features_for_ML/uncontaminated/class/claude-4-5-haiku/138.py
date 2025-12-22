class Response:
    def __init__(self, response_id: str, *, use_elevenlabs: bool | None = None):
        self.response_id = response_id
        self.use_elevenlabs = use_elevenlabs
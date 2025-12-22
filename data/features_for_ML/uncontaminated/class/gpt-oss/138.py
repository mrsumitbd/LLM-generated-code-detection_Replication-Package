class Response:
    def __init__(self, response_id: str, *, use_elevenlabs: bool | None = None):
        self.response_id = response_id
        self.use_elevenlabs = use_elevenlabs if use_elevenlabs is not None else False
        self.content: str | None = None
        self.metadata: dict = {}

    def set_content(self, content: str) -> None:
        self.content = content

    def get_content(self) -> str | None:
        return self.content

    def add_metadata(self, key: str, value) -> None:
        self.metadata[key] = value

    def to_dict(self) -> dict:
        return {
            "response_id": self.response_id,
            "use_elevenlabs": self.use_elevenlabs,
            "content": self.content,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Response":
        obj = cls(data["response_id"], use_elevenlabs=data.get("use_elevenlabs"))
        obj.content = data.get("content")
        obj.metadata = data.get("metadata", {})
        return obj

    def __repr__(self) -> str:
        return (
            f"<Response id={self.response_id!r} "
            f"use_elevenlabs={self.use_elevenlabs!r} "
            f"content={self.content!r}>"
        )
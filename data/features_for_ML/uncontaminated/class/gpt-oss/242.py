class WebhookResourceWithStreamingResponse:
    def __init__(self, webhook: "WebhookResource") -> None:
        self._webhook = webhook

    def __getattr__(self, name):
        return getattr(self._webhook, name)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} wrapping {self._webhook!r}>"
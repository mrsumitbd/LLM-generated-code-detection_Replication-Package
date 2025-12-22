class WebhookResourceWithStreamingResponse:

    def __init__(self, webhook: WebhookResource) -> None:
        self._webhook = webhook

    def __getattr__(self, name: str):
        """Delegate attribute access to the wrapped webhook resource."""
        return getattr(self._webhook, name)
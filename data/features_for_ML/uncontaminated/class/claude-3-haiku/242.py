class WebhookResourceWithStreamingResponse:
    def __init__(self, webhook: WebhookResource) -> None:
        self.webhook = webhook
        self.response_stream = None

    def start_response(self) -> None:
        self.response_stream = self.webhook.start_response()

    def write(self, data: bytes) -> None:
        self.response_stream.write(data)

    def finish(self) -> None:
        self.response_stream.finish()
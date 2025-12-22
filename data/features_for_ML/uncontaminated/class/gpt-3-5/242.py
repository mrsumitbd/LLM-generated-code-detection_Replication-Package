from typing import List

class WebhookResourceWithStreamingResponse:

    def __init__(self, webhook: WebhookResource) -> None:
        self.webhook = webhook

    def send_streaming_response(self, data: List[str]) -> None:
        for item in data:
            self.webhook.send_response(item)

class WebhookResource:
    
    def send_response(self, data: str) -> None:
        print(data)

# Example usage:
webhook_resource = WebhookResource()
webhook_with_streaming_response = WebhookResourceWithStreamingResponse(webhook_resource)
webhook_with_streaming_response.send_streaming_response(["Response 1", "Response 2", "Response 3"])
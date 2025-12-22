class MockCompletion:
    def __init__(self):
        self.id = "mock-completion-1"
        self.object = "text_completion"
        self.created = 1234567890
        self.model = "mock-model"
        self.choices = [
            {
                "text": "This is a mock completion response.",
                "index": 0,
                "logprobs": None,
                "finish_reason": "length"
            }
        ]
        self.usage = {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
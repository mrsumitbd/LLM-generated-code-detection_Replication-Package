import requests

class LLMClient:
    """Manages communication with the LLM provider."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.api_url = "https://api.example.com/v1/chat"

    def get_response(self, messages: list[dict[str, str]]) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "messages": messages
        }

        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()

        return response.json()["response"]
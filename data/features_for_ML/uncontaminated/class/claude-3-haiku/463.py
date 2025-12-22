import requests
import json

class AgentClient:
    """
    Client class for Agent service.
    """

    def __init__(self, config: AgentCfg):
        self.config = config
        self._initialize_agent_model(config)

    def _initialize_agent_model(self, config: AgentCfg):
        self.api_url = config.api_url
        self.api_key = config.api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def __getattr__(self, attr_name: str):
        def wrapper(*args, **kwargs):
            endpoint = f"{self.api_url}/{attr_name}"
            response = requests.request(
                "POST", endpoint, headers=self.headers, json=kwargs
            )
            response.raise_for_status()
            return response.json()
        return wrapper
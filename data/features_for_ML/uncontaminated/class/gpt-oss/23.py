import json
import requests
from typing import Any, Dict

class AzureInferenceChat:
    """An Azure Chat Model provider."""

    def __init__(self, llm_config: Any) -> None:
        """
        Initialize the Azure inference chat client.

        Parameters
        ----------
        llm_config : Any
            Configuration object that must provide the following attributes:
            - endpoint (str): The Azure OpenAI endpoint URL.
            - api_key (str): The API key for authentication.
            - deployment_name (str): The name of the deployment to use.
            - api_version (str, optional): The API version. Defaults to "2023-12-01-preview".
        """
        # Store the configuration
        self.config = llm_config

        # Prepare the HTTP session with authentication headers
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "api-key": getattr(self.config, "api_key", ""),
            }
        )

        # Base URL for the chat completions endpoint
        self.url = (
            f"{getattr(self.config, 'endpoint', '').rstrip('/')}"
            f"/openai/deployments/{getattr(self.config, 'deployment_name', '')}"
            f"/chat/completions?api-version={getattr(self.config, 'api_version', '2023-12-01-preview')}"
        )

        # Internal usage counter
        self._usage: Dict[str, int] = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def _update_usage(self, usage: Dict[str, Any]) -> None:
        """
        Update the internal usage counters based on the response from Azure.

        Parameters
        ----------
        usage : Dict[str, Any]
            The usage dictionary returned by Azure. Expected keys:
            - prompt_tokens
            - completion_tokens
            - total_tokens
        """
        for key in self._usage:
            self._usage[key] += int(usage.get(key, 0))

    def get_usage(self) -> Dict[str, int]:
        """
        Return the cumulative usage statistics.

        Returns
        -------
        Dict[str, int]
            A dictionary containing the total prompt tokens, completion tokens,
            and total tokens used so far.
        """
        return dict(self._usage)

    # Optional helper method to send a chat request
    def chat(self, messages: list[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        """
        Send a chat completion request to Azure OpenAI.

        Parameters
        ----------
        messages : list[Dict[str, str]]
            A list of message dictionaries, each containing 'role' and 'content'.
        **kwargs : Any
            Additional parameters to pass to the Azure API (e.g., temperature, max_tokens).

        Returns
        -------
        Dict[str, Any]
            The JSON response from Azure.
        """
        payload = {"messages": messages, **kwargs}
        response = self.session.post(self.url, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        # Update usage counters if available
        if "usage" in data:
            self._update_usage(data["usage"])

        return data
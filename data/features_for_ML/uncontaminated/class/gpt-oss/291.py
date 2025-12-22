import openai
from typing import List, Dict


class LLMClient:
    """Manages communication with the LLM provider."""

    def __init__(self, api_key: str) -> None:
        """
        Initialize the LLM client with the provided API key.

        Parameters
        ----------
        api_key : str
            The API key for authenticating with the LLM provider.
        """
        openai.api_key = api_key

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Send a list of messages to the LLM and return the assistant's reply.

        Parameters
        ----------
        messages : list[dict[str, str]]
            A list of message dictionaries, each containing a 'role' and 'content' key.

        Returns
        -------
        str
            The content of the assistant's reply.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=512,
                n=1,
                stop=None,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            raise RuntimeError(f"LLM request failed: {exc}") from exc
import json
from typing import Any, Dict, Iterable, List, Optional

import requests


class OllamaClient:
    """Client for interacting with Ollama local LLM service."""

    def __init__(self, settings: Any) -> None:
        """
        Initialize the Ollama client.

        Parameters
        ----------
        settings : Any
            An object that contains configuration attributes. Expected
            attributes are:
                - host (str): Base URL of the Ollama service. Defaults to
                  'http://localhost:11434'.
                - model (str, optional): Default model name to use for
                  requests.
        """
        self.base_url: str = getattr(settings, "host", "http://localhost:11434")
        self.default_model: Optional[str] = getattr(settings, "model", None)
        self.session: requests.Session = requests.Session()

    # ------------------------------------------------------------------
    # Core request helpers
    # ------------------------------------------------------------------
    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON response from {url}") from exc

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate text from a prompt.

        Parameters
        ----------
        prompt : str
            The prompt to send to the model.
        model : str, optional
            The model name to use. Falls back to the default model.
        temperature : float, optional
            Sampling temperature.
        top_p : float, optional
            Nucleus sampling parameter.
        max_tokens : int, optional
            Maximum number of tokens to generate.
        stream : bool, default False
            Whether to stream the response.
        **kwargs : Any
            Additional parameters forwarded to the Ollama API.

        Returns
        -------
        dict
            Parsed JSON response from the Ollama service.
        """
        payload: Dict[str, Any] = {"prompt": prompt}
        if model is not None:
            payload["model"] = model
        elif self.default_model is not None:
            payload["model"] = self.default_model

        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        payload["stream"] = stream

        payload.update(kwargs)
        return self._post("/api/generate", payload)

    def chat(
        self,
        messages: Iterable[Dict[str, str]],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Chat with the model using a list of messages.

        Parameters
        ----------
        messages : Iterable[Dict[str, str]]
            List of message dicts with keys 'role' and 'content'.
        model : str, optional
            The model name to use. Falls back to the default model.
        temperature : float, optional
            Sampling temperature.
        top_p : float, optional
            Nucleus sampling parameter.
        max_tokens : int, optional
            Maximum number of tokens to generate.
        stream : bool, default False
            Whether to stream the response.
        **kwargs : Any
            Additional parameters forwarded to the Ollama API.

        Returns
        -------
        dict
            Parsed JSON response from the Ollama service.
        """
        payload: Dict[str, Any] = {"messages": list(messages)}
        if model is not None:
            payload["model"] = model
        elif self.default_model is not None:
            payload["model"] = self.default_model

        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        payload["stream"] = stream

        payload.update(kwargs)
        return self._post("/api/chat", payload)

    def list_models(self) -> List[Dict[str, Any]]:
        """
        Retrieve a list of available models from the Ollama service.

        Returns
        -------
        list[dict]
            Each dict contains model metadata.
        """
        return self._post("/api/tags", {})

    def pull_model(self, model: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Pull a model from the Ollama registry.

        Parameters
        ----------
        model : str
            Name of the model to pull.
        **kwargs : Any
            Additional parameters forwarded to the Ollama API.

        Returns
        -------
        dict
            Parsed JSON response from the Ollama service.
        """
        payload: Dict[str, Any] = {"name": model}
        payload.update(kwargs)
        return self._post("/api/pull", payload)

    def delete_model(self, model: str) -> Dict[str, Any]:
        """
        Delete a model from the local Ollama instance.

        Parameters
        ----------
        model : str
            Name of the model to delete.

        Returns
        -------
        dict
            Parsed JSON response from the Ollama service.
        """
        payload: Dict[str, Any] = {"name": model}
        return self._post("/api/delete", payload)
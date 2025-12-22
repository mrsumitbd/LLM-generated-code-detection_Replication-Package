import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from urllib.parse import urljoin

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class AgentCard:
    """
    Simple wrapper around the raw agent card JSON.
    """
    data: Dict[str, Any]

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)


class A2ACardResolver:
    """
    Resolve an Agent Card from a base URL.

    Parameters
    ----------
    base_url : str
        The base URL of the agent (e.g. "https://example.com").
    agent_card_path : str, optional
        The relative path to the agent card. Defaults to "/.well-known/agent.json".
    """

    def __init__(self, base_url: str, agent_card_path: str = "/.well-known/agent.json") -> None:
        self.base_url = base_url.rstrip("/")
        self.agent_card_path = agent_card_path
        self._agent_card: Optional[AgentCard] = None

    def _fetch_agent_card(self) -> Dict[str, Any]:
        url = urljoin(self.base_url + "/", self.agent_card_path.lstrip("/"))
        log.debug("Fetching agent card from %s", url)
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to fetch agent card from {url}") from exc

        try:
            data = resp.json()
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in agent card at {url}") from exc

        if not isinstance(data, dict):
            raise ValueError(f"Agent card JSON must be an object, got {type(data).__name__}")

        return data

    def get_agent_card(self) -> AgentCard:
        """
        Retrieve the agent card, caching the result for subsequent calls.

        Returns
        -------
        AgentCard
            The resolved agent card.
        """
        if self._agent_card is None:
            raw = self._fetch_agent_card()
            self._agent_card = AgentCard(data=raw)
        return self._agent_card
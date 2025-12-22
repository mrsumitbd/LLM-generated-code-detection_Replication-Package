from typing import Dict

class AsyncAgentApiClient:
    """Async client for interacting with the Automagik Agents API."""

    def __init__(self, config_override=None):
        pass

    def _make_headers(self, accept_sse: bool = False) -> Dict[str, str]:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'AsyncAgentApiClient'
        }
        if accept_sse:
            headers['Accept'] = 'text/event-stream'
        return headers
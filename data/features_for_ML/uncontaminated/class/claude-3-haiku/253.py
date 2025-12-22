import aiohttp
import asyncio
from typing import Dict

class AsyncAgentApiClient:
    """Async client for interacting with the Automagik Agents API."""

    def __init__(self, config_override=None):
        self.config_override = config_override
        self.session = None

    async def _create_session(self):
        self.session = aiohttp.ClientSession()

    async def _close_session(self):
        await self.session.close()

    def _make_headers(self, accept_sse: bool = False) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if accept_sse:
            headers["Accept"] = "text/event-stream"
        return headers

    async def get_agents(self):
        async with self.session.get("/agents", headers=self._make_headers()) as response:
            response.raise_for_status()
            return await response.json()

    async def get_agent_by_id(self, agent_id: str):
        async with self.session.get(f"/agents/{agent_id}", headers=self._make_headers()) as response:
            response.raise_for_status()
            return await response.json()

    async def create_agent(self, agent_data: Dict):
        async with self.session.post("/agents", headers=self._make_headers(), json=agent_data) as response:
            response.raise_for_status()
            return await response.json()

    async def update_agent(self, agent_id: str, agent_data: Dict):
        async with self.session.put(f"/agents/{agent_id}", headers=self._make_headers(), json=agent_data) as response:
            response.raise_for_status()
            return await response.json()

    async def delete_agent(self, agent_id: str):
        async with self.session.delete(f"/agents/{agent_id}", headers=self._make_headers()) as response:
            response.raise_for_status()

    async def get_agent_events(self, agent_id: str):
        async with self.session.get(f"/agents/{agent_id}/events", headers=self._make_headers(accept_sse=True)) as response:
            response.raise_for_status()
            async for event in response.content:
                yield event
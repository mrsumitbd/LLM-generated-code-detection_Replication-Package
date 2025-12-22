import os
import json
import aiohttp
from typing import Dict, Optional, Any, AsyncGenerator
from datetime import datetime


class AsyncAgentApiClient:
    """Async client for interacting with the Automagik Agents API."""

    def __init__(self, config_override=None):
        self.config = config_override or {}
        self.base_url = self.config.get('base_url', os.getenv('AGENT_API_BASE_URL', 'https://api.automagik.ai'))
        self.api_key = self.config.get('api_key', os.getenv('AGENT_API_KEY', ''))
        self.timeout = self.config.get('timeout', 30)
        self.session: Optional[aiohttp.ClientSession] = None

    def _make_headers(self, accept_sse: bool = False) -> Dict[str, str]:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'AsyncAgentApiClient/1.0',
        }
        
        if accept_sse:
            headers['Accept'] = 'text/event-stream'
        else:
            headers['Accept'] = 'application/json'
        
        return headers

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def create_agent(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        session = await self._get_session()
        url = f'{self.base_url}/agents'
        headers = self._make_headers()
        
        async with session.post(url, json=agent_config, headers=headers, timeout=self.timeout) as resp:
            return await resp.json()

    async def get_agent(self, agent_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f'{self.base_url}/agents/{agent_id}'
        headers = self._make_headers()
        
        async with session.get(url, headers=headers, timeout=self.timeout) as resp:
            return await resp.json()

    async def list_agents(self) -> Dict[str, Any]:
        session = await self._get_session()
        url = f'{self.base_url}/agents'
        headers = self._make_headers()
        
        async with session.get(url, headers=headers, timeout=self.timeout) as resp:
            return await resp.json()

    async def update_agent(self, agent_id: str, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        session = await self._get_session()
        url = f'{self.base_url}/agents/{agent_id}'
        headers = self._make_headers()
        
        async with session.put(url, json=agent_config, headers=headers, timeout=self.timeout) as resp:
            return await resp.json()

    async def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        session = await self._get_session()
        url = f'{self.base_url}/agents/{agent_id}'
        headers = self._make_headers()
        
        async with session.delete(url, headers=headers, timeout=self.timeout) as resp:
            return await resp.json()

    async def execute_agent(self, agent_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        session = await self._get_session()
        url = f'{self.base_url}/agents/{agent_id}/execute'
        headers = self._make_headers()
        
        async with session.post(url, json=input_data, headers=headers, timeout=self.timeout) as resp:
            return await resp.json()

    async def stream_agent_execution(self, agent_id: str, input_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        session = await self._get_session()
        url = f'{self.base_url}/agents/{agent_id}/stream'
        headers = self._make_headers(accept_sse=True)
        
        async with session.post(url, json=input_data, headers=headers, timeout=self.timeout) as resp:
            async for line in resp.content:
                if line:
                    yield line.decode('utf-8').strip()
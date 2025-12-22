import aiohttp
import asyncio
from typing import Optional, Any, Dict
from anthropic import Anthropic

class SessionManager:
    """Manages HTTP sessions with authentication"""

    def __init__(self, config: 'FOClientConfig', auth_manager: 'AuthenticationManager'):
        self.config = config
        self.auth_manager = auth_manager
        self.session: Optional[aiohttp.ClientSession] = None
        self.client = Anthropic()
        self._lock = asyncio.Lock()

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session with authentication headers"""
        if self.session is None or self.session.closed:
            headers = await self.auth_manager.get_headers()
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session

    async def close(self) -> None:
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def request(
        self,
        method: str,
        url: str,
        **kwargs: Any
    ) -> aiohttp.ClientResponse:
        """Make an authenticated HTTP request"""
        session = await self.get_session()
        return await session.request(method, url, **kwargs)

    async def get(self, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make a GET request"""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make a POST request"""
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make a PUT request"""
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make a DELETE request"""
        return await self.request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make a PATCH request"""
        return await self.request("PATCH", url, **kwargs)

    def chat(self, messages: list[Dict[str, str]], **kwargs: Any) -> Any:
        """Send a chat message using Claude"""
        return self.client.messages.create(
            model=self.config.model,
            messages=messages,
            **kwargs
        )

    async def __aenter__(self) -> 'SessionManager':
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit"""
        await self.close()
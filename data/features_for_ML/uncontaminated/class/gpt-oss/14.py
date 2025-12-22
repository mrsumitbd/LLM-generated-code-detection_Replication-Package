from __future__ import annotations

from typing import Any


class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: Any) -> None:
        self._agents = agents

    async def retrieve(self, id: str, *, stripe_version: str | None = None, **params) -> Any:
        return await self._agents.retrieve(id, stripe_version=stripe_version, **params)

    async def list(self, *, stripe_version: str | None = None, **params) -> Any:
        return await self._agents.list(stripe_version=stripe_version, **params)

    async def create(self, *, stripe_version: str | None = None, **params) -> Any:
        return await self._agents.create(stripe_version=stripe_version, **params)

    async def update(self, id: str, *, stripe_version: str | None = None, **params) -> Any:
        return await self._agents.update(id, stripe_version=stripe_version, **params)

    async def delete(self, id: str, *, stripe_version: str | None = None, **params) -> Any:
        return await self._agents.delete(id, stripe_version=stripe_version, **params)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._agents, name)
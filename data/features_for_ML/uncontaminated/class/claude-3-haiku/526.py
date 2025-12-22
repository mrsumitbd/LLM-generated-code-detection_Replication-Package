import asyncio
from typing import AsyncGenerator

class AsyncTrendingSearchResourceWithStreamingResponse:
    def __init__(self, trending_search: AsyncTrendingSearchResource) -> None:
        self.trending_search = trending_search

    async def get_trending_searches(self, limit: int = 10) -> AsyncGenerator[str, None]:
        search_terms = await self.trending_search.get_trending_searches(limit)
        for term in search_terms:
            yield term
            await asyncio.sleep(0.1)
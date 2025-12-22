from typing import List
from async_trending_search_resource import AsyncTrendingSearchResource

class AsyncTrendingSearchResourceWithStreamingResponse:

    def __init__(self, trending_search: AsyncTrendingSearchResource) -> None:
        self.trending_search = trending_search

    async def get_trending_searches(self) -> List[str]:
        return await self.trending_search.get_trending_searches()
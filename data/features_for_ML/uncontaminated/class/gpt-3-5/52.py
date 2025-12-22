from typing import List
from async_categories_resource import AsyncCategoriesResource

class AsyncCategoriesResourceWithRawResponse:

    def __init__(self, categories: AsyncCategoriesResource) -> None:
        self.categories = categories

    async def get_categories(self) -> List[str]:
        raw_response = await self.categories.fetch_categories()
        return raw_response
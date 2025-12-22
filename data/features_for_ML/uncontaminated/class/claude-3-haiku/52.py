class AsyncCategoriesResourceWithRawResponse:
    def __init__(self, categories: AsyncCategoriesResource) -> None:
        self.categories = categories

    async def get_categories(self) -> dict:
        response = await self.categories.get_categories()
        return response.json()

    async def get_category(self, category_id: str) -> dict:
        response = await self.categories.get_category(category_id)
        return response.json()

    async def create_category(self, data: dict) -> dict:
        response = await self.categories.create_category(data)
        return response.json()

    async def update_category(self, category_id: str, data: dict) -> dict:
        response = await self.categories.update_category(category_id, data)
        return response.json()

    async def delete_category(self, category_id: str) -> dict:
        response = await self.categories.delete_category(category_id)
        return response.json()
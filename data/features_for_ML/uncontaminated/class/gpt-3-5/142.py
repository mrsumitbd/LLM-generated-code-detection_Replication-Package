from typing import Any
from async_models_resource import AsyncModelsResource

class AsyncModelsResourceWithRawResponse:

    def __init__(self, models: AsyncModelsResource) -> None:
        self.models = models

    async def get_model(self, model_id: str) -> Any:
        return await self.models.get_model(model_id)

    async def create_model(self, model_data: dict) -> Any:
        return await self.models.create_model(model_data)

    async def update_model(self, model_id: str, model_data: dict) -> Any:
        return await self.models.update_model(model_id, model_data)

    async def delete_model(self, model_id: str) -> Any:
        return await self.models.delete_model(model_id)
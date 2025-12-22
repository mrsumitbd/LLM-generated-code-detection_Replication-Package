class AsyncModelsResourceWithRawResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self.models = models

    async def get_model(self, model_id: str) -> Tuple[Any, requests.Response]:
        response = await self.models.get_model(model_id)
        return response.json(), response

    async def create_model(self, model_data: Dict[str, Any]) -> Tuple[Any, requests.Response]:
        response = await self.models.create_model(model_data)
        return response.json(), response

    async def update_model(self, model_id: str, model_data: Dict[str, Any]) -> Tuple[Any, requests.Response]:
        response = await self.models.update_model(model_id, model_data)
        return response.json(), response

    async def delete_model(self, model_id: str) -> Tuple[Any, requests.Response]:
        response = await self.models.delete_model(model_id)
        return response.json(), response
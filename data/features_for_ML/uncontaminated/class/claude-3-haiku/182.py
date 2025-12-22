class AsyncFunctionsResourceWithRawResponse:
    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self.functions = functions

    async def call(self, function_name: str, **kwargs) -> bytes:
        response = await self.functions.call(function_name, **kwargs)
        return response.content

    async def call_with_status(self, function_name: str, **kwargs) -> tuple[bytes, int]:
        response = await self.functions.call(function_name, **kwargs)
        return response.content, response.status_code

    async def call_with_headers(self, function_name: str, **kwargs) -> tuple[bytes, dict[str, str]]:
        response = await self.functions.call(function_name, **kwargs)
        return response.content, response.headers
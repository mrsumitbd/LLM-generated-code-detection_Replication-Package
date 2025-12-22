from typing import Any
from async_functions_resource import AsyncFunctionsResource

class AsyncFunctionsResourceWithRawResponse:

    def __init__(self, functions: AsyncFunctionsResource) -> None:
        self.functions = functions

    async def get_raw_response(self, function_name: str, *args: Any, **kwargs: Any) -> Any:
        return await self.functions.get_raw_response(function_name, *args, **kwargs)
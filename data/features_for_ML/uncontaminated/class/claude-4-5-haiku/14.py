class AsyncAgentsResourceWithRawResponse:

    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

    @property
    def create(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return async_to_raw_response(self._agents.create)

    @property
    def retrieve(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return async_to_raw_response(self._agents.retrieve)

    @property
    def update(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return async_to_raw_response(self._agents.update)

    @property
    def list(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return async_to_raw_response(self._agents.list)

    @property
    def delete(self) -> Callable[..., Awaitable[BinaryAPIResponse]]:
        return async_to_raw_response(self._agents.delete)
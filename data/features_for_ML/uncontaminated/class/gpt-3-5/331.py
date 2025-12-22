from async_reducto import AsyncReducto

class AsyncAPIResource:

    def __init__(self, client: AsyncReducto) -> None:
        self.client = client
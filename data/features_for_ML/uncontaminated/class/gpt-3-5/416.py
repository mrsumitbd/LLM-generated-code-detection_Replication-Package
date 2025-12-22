class AsyncInfoResourceWithRawResponse:
    
    def __init__(self, info: AsyncInfoResource) -> None:
        self.info = info

    def get_info(self) -> str:
        return self.info.get_info()

    def get_raw_response(self) -> str:
        return self.info.get_raw_response()
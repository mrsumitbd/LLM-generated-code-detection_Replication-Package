class AsyncInfoResourceWithRawResponse:
    def __init__(self, info: AsyncInfoResource) -> None:
        self._info = info
        self._raw_response = None

    @property
    def raw_response(self):
        if self._raw_response is None:
            self._raw_response = self._info.get_raw_response()
        return self._raw_response

    @property
    def status(self):
        return self._info.status

    @property
    def data(self):
        return self._info.data

    @property
    def headers(self):
        return self._info.headers

    @property
    def url(self):
        return self._info.url

    @property
    def request(self):
        return self._info.request
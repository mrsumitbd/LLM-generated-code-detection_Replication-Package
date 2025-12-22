class RequestAttributes:
    """
    The RequestAttributes class is responsible for managing user http and webscoket session
    metadata. It provides a way to store and expose session attributes to workflow tools.
    """

    def __init__(self, method=None, url_path=None, url_port=None, url_scheme=None, headers=None,
                 query_params=None, path_params=None, client_host=None, client_port=None, cookies=None) -> None:
        self._method = method
        self._url_path = url_path
        self._url_port = url_port
        self._url_scheme = url_scheme
        self._headers = headers
        self._query_params = query_params
        self._path_params = path_params
        self._client_host = client_host
        self._client_port = client_port
        self._cookies = cookies

    @property
    def method(self) -> str | None:
        return self._method

    @property
    def url_path(self) -> str | None:
        return self._url_path

    @property
    def url_port(self) -> int | None:
        return self._url_port

    @property
    def url_scheme(self) -> str | None:
        return self._url_scheme

    @property
    def headers(self) -> Headers | None:
        return self._headers

    @property
    def query_params(self) -> QueryParams | None:
        return self._query_params

    @property
    def path_params(self) -> dict[str, str] | None:
        return self._path_params

    @property
    def client_host(self) -> str | None:
        return self._client_host

    @property
    def client_port(self) -> int | None:
        return self._client_port

    @property
    def cookies(self) -> dict[str, str] | None:
        return self._cookies
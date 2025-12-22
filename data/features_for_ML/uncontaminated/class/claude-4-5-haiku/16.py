class RequestAttributes:
    """
    The RequestAttributes class is responsible for managing user http and webscoket session
    metadata. It provides a way to store and expose session attributes to workflow tools.
    """

    def __init__(self) -> None:
        self._method: str | None = None
        self._url_path: str | None = None
        self._url_port: int | None = None
        self._url_scheme: str | None = None
        self._headers: Headers | None = None
        self._query_params: QueryParams | None = None
        self._path_params: dict[str, str] | None = None
        self._client_host: str | None = None
        self._client_port: int | None = None
        self._cookies: dict[str, str] | None = None

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
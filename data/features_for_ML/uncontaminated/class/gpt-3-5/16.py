from typing import Union, Dict

class RequestAttributes:
    """
    The RequestAttributes class is responsible for managing user http and webscoket session
    metadata. It provides a way to store and expose session attributes to workflow tools.
    """

    def __init__(self) -> None:
        self._method: Union[str, None] = None
        self._url_path: Union[str, None] = None
        self._url_port: Union[int, None] = None
        self._url_scheme: Union[str, None] = None
        self._headers: Union[Headers, None] = None
        self._query_params: Union[QueryParams, None] = None
        self._path_params: Union[Dict[str, str], None] = None
        self._client_host: Union[str, None] = None
        self._client_port: Union[int, None] = None
        self._cookies: Union[Dict[str, str], None] = None

    @property
    def method(self) -> Union[str, None]:
        return self._method

    @property
    def url_path(self) -> Union[str, None]:
        return self._url_path

    @property
    def url_port(self) -> Union[int, None]:
        return self._url_port

    @property
    def url_scheme(self) -> Union[str, None]:
        return self._url_scheme

    @property
    def headers(self) -> Union[Headers, None]:
        return self._headers

    @property
    def query_params(self) -> Union[QueryParams, None]:
        return self._query_params

    @property
    def path_params(self) -> Union[Dict[str, str], None]:
        return self._path_params

    @property
    def client_host(self) -> Union[str, None]:
        return self._client_host

    @property
    def client_port(self) -> Union[int, None]:
        return self._client_port

    @property
    def cookies(self) -> Union[Dict[str, str], None]:
        return self._cookies
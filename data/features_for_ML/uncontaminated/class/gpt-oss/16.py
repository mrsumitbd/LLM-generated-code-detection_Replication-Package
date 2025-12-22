from __future__ import annotations

from typing import Any, Dict, Optional

# Alias types for compatibility with frameworks that provide these classes.
Headers = Any
QueryParams = Any


class RequestAttributes:
    """
    The RequestAttributes class is responsible for managing user http and websocket session
    metadata. It provides a way to store and expose session attributes to workflow tools.
    """

    def __init__(self) -> None:
        self._method: Optional[str] = None
        self._url_path: Optional[str] = None
        self._url_port: Optional[int] = None
        self._url_scheme: Optional[str] = None
        self._headers: Optional[Headers] = None
        self._query_params: Optional[QueryParams] = None
        self._path_params: Optional[Dict[str, str]] = None
        self._client_host: Optional[str] = None
        self._client_port: Optional[int] = None
        self._cookies: Optional[Dict[str, str]] = None

    @property
    def method(self) -> Optional[str]:
        return self._method

    @method.setter
    def method(self, value: str) -> None:
        self._method = value

    @property
    def url_path(self) -> Optional[str]:
        return self._url_path

    @url_path.setter
    def url_path(self, value: str) -> None:
        self._url_path = value

    @property
    def url_port(self) -> Optional[int]:
        return self._url_port

    @url_port.setter
    def url_port(self, value: int) -> None:
        self._url_port = value

    @property
    def url_scheme(self) -> Optional[str]:
        return self._url_scheme

    @url_scheme.setter
    def url_scheme(self, value: str) -> None:
        self._url_scheme = value

    @property
    def headers(self) -> Optional[Headers]:
        return self._headers

    @headers.setter
    def headers(self, value: Headers) -> None:
        self._headers = value

    @property
    def query_params(self) -> Optional[QueryParams]:
        return self._query_params

    @query_params.setter
    def query_params(self, value: QueryParams) -> None:
        self._query_params = value

    @property
    def path_params(self) -> Optional[Dict[str, str]]:
        return self._path_params

    @path_params.setter
    def path_params(self, value: Dict[str, str]) -> None:
        self._path_params = value

    @property
    def client_host(self) -> Optional[str]:
        return self._client_host

    @client_host.setter
    def client_host(self, value: str) -> None:
        self._client_host = value

    @property
    def client_port(self) -> Optional[int]:
        return self._client_port

    @client_port.setter
    def client_port(self, value: int) -> None:
        self._client_port = value

    @property
    def cookies(self) -> Optional[Dict[str, str]]:
        return self._cookies

    @cookies.setter
    def cookies(self, value: Dict[str, str]) -> None:
        self._cookies = value

    def __repr__(self) -> str:
        attrs = (
            f"method={self._method!r}, "
            f"url_path={self._url_path!r}, "
            f"url_port={self._url_port!r}, "
            f"url_scheme={self._url_scheme!r}, "
            f"headers={self._headers!r}, "
            f"query_params={self._query_params!r}, "
            f"path_params={self._path_params!r}, "
            f"client_host={self._client_host!r}, "
            f"client_port={self._client_port!r}, "
            f"cookies={self._cookies!r}"
        )
        return f"{self.__class__.__name__}({attrs})"
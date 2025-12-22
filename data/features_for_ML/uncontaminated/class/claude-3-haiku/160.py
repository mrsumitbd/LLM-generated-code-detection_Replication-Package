import logging

class FletXPage:
    pass

class RouteConfig:
    """
    Route Configuration Manager responsible for managing route configuration.
    """

    _routes = {}
    _logger = logging.getLogger(__name__)

    @classmethod
    @property
    def logger(cls):
        return cls._logger

    @classmethod
    def register_routes(cls, routes: Dict[str, Type[FletXPage]]):
        cls._routes.update(routes)

    @classmethod
    def register_route(cls, path: str, page_class: Type[FletXPage]):
        cls._routes[path] = page_class

    @classmethod
    def get_routes(cls) -> Dict[str, Type[FletXPage]]:
        return cls._routes.copy()

    @classmethod
    def get_route(cls, path: str) -> Type[FletXPage]:
        return cls._routes[path]
from typing import Dict, Type

class RouteConfig:
    """
    Route Configuration Manager responsible for managing route configuration.
    """

    _routes: Dict[str, Type[FletXPage]] = {}

    @classmethod
    @property
    def logger(cls):
        pass

    @classmethod
    def register_routes(cls, routes: Dict[str, Type[FletXPage]]):
        cls._routes.update(routes)

    @classmethod
    def register_route(cls, path: str, page_class: Type[FletXPage]):
        cls._routes[path] = page_class

    @classmethod
    def get_routes(cls) -> Dict[str, Type[FletXPage]]:
        return cls._routes

    @classmethod
    def get_route(cls, path: str) -> Type[FletXPage]:
        return cls._routes.get(path)
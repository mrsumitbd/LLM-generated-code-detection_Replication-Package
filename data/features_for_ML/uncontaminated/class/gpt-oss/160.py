import logging
from typing import Dict, Type

# Assuming FletXPage is defined elsewhere in the project
try:
    from fletx import FletXPage  # Adjust import path as needed
except Exception:
    # Fallback placeholder if the actual import fails during testing
    class FletXPage:
        pass


class RouteConfig:
    """
    Route Configuration Manager responsible for managing route configuration.
    """

    _routes: Dict[str, Type[FletXPage]] = {}

    @classmethod
    @property
    def logger(cls) -> logging.Logger:
        """
        Returns a logger instance for the RouteConfig class.
        """
        return logging.getLogger(cls.__name__)

    @classmethod
    def register_routes(cls, routes: Dict[str, Type[FletXPage]]) -> None:
        """
        Register multiple routes at once.

        Args:
            routes: A dictionary mapping path strings to page classes.
        """
        if not isinstance(routes, dict):
            cls.logger.error("register_routes expects a dict, got %s", type(routes))
            raise TypeError("routes must be a dict")
        for path, page_cls in routes.items():
            cls.register_route(path, page_cls)

    @classmethod
    def register_route(cls, path: str, page_class: Type[FletXPage]) -> None:
        """
        Register a single route.

        Args:
            path: The URL path for the route.
            page_class: The page class to instantiate for this route.
        """
        if not isinstance(path, str):
            cls.logger.error("Route path must be a string, got %s", type(path))
            raise TypeError("path must be a string")
        if not isinstance(page_class, type):
            cls.logger.error("page_class must be a class, got %s", type(page_class))
            raise TypeError("page_class must be a class")
        if not issubclass(page_class, FletXPage):
            cls.logger.error(
                "page_class %s must inherit from FletXPage", page_class.__name__
            )
            raise TypeError("page_class must inherit from FletXPage")
        cls._routes[path] = page_class
        cls.logger.debug("Registered route: %s -> %s", path, page_class.__name__)

    @classmethod
    def get_routes(cls) -> Dict[str, Type[FletXPage]]:
        """
        Return a copy of the registered routes dictionary.
        """
        return dict(cls._routes)

    @classmethod
    def get_route(cls, path: str) -> Type[FletXPage]:
        """
        Retrieve the page class associated with a given path.

        Args:
            path: The URL path to look up.

        Returns:
            The page class registered for the path.

        Raises:
            KeyError: If the path is not registered.
        """
        try:
            return cls._routes[path]
        except KeyError:
            cls.logger.error("Route not found for path: %s", path)
            raise
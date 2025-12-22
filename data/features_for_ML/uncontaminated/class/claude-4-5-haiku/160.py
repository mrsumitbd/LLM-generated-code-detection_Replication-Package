import logging
from typing import Dict, Type, Optional

class RouteConfig:
    """
    Route Configuration Manager responsible for managing route configuration.
    """
    
    _routes: Dict[str, Type['FletXPage']] = {}
    _logger: Optional[logging.Logger] = None

    @classmethod
    @property
    def logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    @classmethod
    def register_routes(cls, routes: Dict[str, Type['FletXPage']]):
        """Register multiple routes at once."""
        if not isinstance(routes, dict):
            cls.logger.warning("Routes must be a dictionary")
            return
        
        for path, page_class in routes.items():
            cls.register_route(path, page_class)

    @classmethod
    def register_route(cls, path: str, page_class: Type['FletXPage']):
        """Register a single route."""
        if not isinstance(path, str) or not path:
            cls.logger.warning(f"Invalid path: {path}")
            return
        
        if path in cls._routes:
            cls.logger.warning(f"Route '{path}' is already registered. Overwriting.")
        
        cls._routes[path] = page_class
        cls.logger.debug(f"Route '{path}' registered with {page_class.__name__}")

    @classmethod
    def get_routes(cls) -> Dict[str, Type['FletXPage']]:
        """Get all registered routes."""
        return cls._routes.copy()

    @classmethod
    def get_route(cls, path: str) -> Type['FletXPage']:
        """Get a specific route by path."""
        if path not in cls._routes:
            cls.logger.warning(f"Route '{path}' not found")
            return None
        
        return cls._routes[path]
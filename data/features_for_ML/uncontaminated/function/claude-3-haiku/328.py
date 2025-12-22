import os
import sys
import importlib
from typing import Any, Dict

def get_middleware_info() -> Dict[str, Any]:
    middleware_info = {}
    
    # Get the list of installed middleware
    installed_middleware = [m for m in sys.modules if m.startswith('django.middleware')]
    
    for middleware_name in installed_middleware:
        try:
            # Import the middleware module
            middleware_module = importlib.import_module(middleware_name)
            
            # Get the middleware class
            middleware_class = getattr(middleware_module, middleware_name.split('.')[-1])
            
            # Get the middleware information
            middleware_info[middleware_name] = {
                'name': middleware_name,
                'description': middleware_class.__doc__ or '',
                'version': getattr(middleware_module, '__version__', 'Unknown'),
                'author': getattr(middleware_module, '__author__', 'Unknown'),
                'license': getattr(middleware_module, '__license__', 'Unknown'),
            }
        except (ImportError, AttributeError):
            # Skip the middleware if there's an issue with importing or getting the information
            pass
    
    return middleware_info
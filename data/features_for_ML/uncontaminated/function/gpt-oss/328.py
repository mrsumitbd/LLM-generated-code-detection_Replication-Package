from typing import Any, Dict

def get_middleware_info() -> Dict[str, Any]:
    """
    Return information about the middleware configured in the current environment.
    If Django is available, it will return the list of middleware classes and the count.
    Otherwise, it returns an empty list and a count of 0.
    """
    info: Dict[str, Any] = {}
    try:
        # Try to import Django settings
        from django.conf import settings  # type: ignore

        # Django 3.x+ uses MIDDLEWARE
        middleware = getattr(settings, "MIDDLEWARE", None)
        if middleware is None:
            # Fallback to older Django versions
            middleware = getattr(settings, "MIDDLEWARE_CLASSES", [])
        # Ensure we have a list
        middleware_list = list(middleware)
        info["middleware"] = middleware_list
        info["count"] = len(middleware_list)
    except Exception:
        # If Django is not installed or settings are not configured
        info["middleware"] = []
        info["count"] = 0

    return info
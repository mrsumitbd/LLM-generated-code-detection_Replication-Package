import traceback
from typing import Any, Type, Union

def _get_exception_context(exc_type: Type[BaseException], exc_value: BaseException, tb: Any) -> dict[str, Any]:
    """Extract relevant context from an exception for logging.

    Args:
        exc_type: The exception type
        exc_value: The exception instance
        tb: The traceback object

    Returns:
        Dictionary with exception context for structured logging
    """
    exception_context = {
        "exception_type": exc_type.__name__,
        "exception_message": str(exc_value),
        "traceback": traceback.format_tb(tb),
    }

    if hasattr(exc_value, "context"):
        exception_context["context"] = exc_value.context

    if hasattr(exc_value, "data"):
        exception_context["data"] = exc_value.data

    return exception_context
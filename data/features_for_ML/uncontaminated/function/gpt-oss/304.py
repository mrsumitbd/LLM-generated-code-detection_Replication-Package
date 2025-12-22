import traceback
from typing import Any, Dict

def _get_exception_context(exc_type: type[BaseException], exc_value: BaseException, tb: Any) -> dict[str, Any]:
    """Extract relevant context from an exception for logging.

    Args:
        exc_type: The exception type
        exc_value: The exception instance
        tb: The traceback object

    Returns:
        Dictionary with exception context for structured logging
    """
    # Basic exception information
    context: Dict[str, Any] = {
        "type": exc_type.__name__,
        "message": str(exc_value),
    }

    # Extract stack frames (filename, line number, function name, source line)
    stack_frames = []
    for frame in traceback.extract_tb(tb or []):
        stack_frames.append(
            {
                "filename": frame.filename,
                "lineno": frame.lineno,
                "name": frame.name,
                "line": frame.line,
            }
        )
    context["stack"] = stack_frames

    # Full formatted traceback string for debugging
    context["traceback"] = "".join(traceback.format_exception(exc_type, exc_value, tb))

    return context
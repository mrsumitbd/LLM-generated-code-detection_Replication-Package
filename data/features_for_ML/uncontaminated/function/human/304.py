import sys
from codegen.cli.telemetry.otel_setup import get_session_uuid, get_otel_logging_handler
from typing import Any
import traceback

def _get_exception_context(exc_type: type[BaseException], exc_value: BaseException, tb: Any) -> dict[str, Any]:
    """Extract relevant context from an exception for logging.

    Args:
        exc_type: The exception type
        exc_value: The exception instance
        tb: The traceback object

    Returns:
        Dictionary with exception context for structured logging
    """
    context = {
        "operation": "cli.unhandled_exception",
        "exception_type": exc_type.__name__,
        "exception_message": str(exc_value),
        "session_id": get_session_uuid(),
    }

    # Add module and function information from the traceback
    if tb is not None:
        # Get the last frame (where the exception occurred)
        last_frame = tb
        while last_frame.tb_next is not None:
            last_frame = last_frame.tb_next

        frame = last_frame.tb_frame
        context.update(
            {
                "exception_file": frame.f_code.co_filename,
                "exception_function": frame.f_code.co_name,
                "exception_line": last_frame.tb_lineno,
            }
        )

        # Get the full stack trace as a string
        context["stack_trace"] = "".join(traceback.format_exception(exc_type, exc_value, tb))

        # Add command context if available from CLI args
        try:
            # Try to extract command information from sys.argv
            if len(sys.argv) > 1:
                context["cli_command"] = sys.argv[1]
                context["cli_args"] = sys.argv[2:] if len(sys.argv) > 2 else []
        except Exception:
            # Don't let context extraction break exception logging
            pass

    return context
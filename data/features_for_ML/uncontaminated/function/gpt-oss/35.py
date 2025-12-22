import logging
from typing import Any

def _log_debug_end(translator: Any, variables: Any) -> None:
    """
    Log the final state of the translator and graph variables for debugging purposes.
    """
    # Try to use the translator's own logger if available, otherwise fall back to the module logger.
    logger = getattr(translator, "logger", logging.getLogger(__name__))

    # Prepare a readable representation of the translator and variables.
    try:
        translator_repr = repr(translator)
    except Exception:
        translator_repr = f"<unrepresentable translator: {type(translator).__name__}>"

    try:
        variables_repr = repr(variables)
    except Exception:
        variables_repr = f"<unrepresentable variables: {type(variables).__name__}>"

    # Log the debug information.
    logger.debug(
        "Debug end: translator=%s, variables=%s",
        translator_repr,
        variables_repr,
    )
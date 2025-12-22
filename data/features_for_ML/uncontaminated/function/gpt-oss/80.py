from typing import List, Optional

def extract_exception_chain(exception: Exception) -> List[str]:
    """
    Extract the full exception chain for detailed error reporting.

    Args:
        exception: The exception to extract the chain from

    Returns:
        List of exception messages in the chain, from most specific to root cause
    """
    chain: List[str] = []
    current: Optional[BaseException] = exception

    while current is not None:
        # Append the message of the current exception
        chain.append(str(current))

        # Determine the next exception in the chain
        # Prefer __cause__ over __context__ if present
        if getattr(current, "__cause__", None) is not None:
            current = current.__cause__
        elif getattr(current, "__context__", None) is not None and not getattr(current, "__suppress_context__", False):
            current = current.__context__
        else:
            current = None

    return chain
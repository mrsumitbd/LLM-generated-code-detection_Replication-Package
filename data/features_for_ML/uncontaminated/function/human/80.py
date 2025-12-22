from typing import Any, Dict, List, Optional, Tuple, Union

def extract_exception_chain(exception: Exception) -> List[str]:
    """
    Extract the full exception chain for detailed error reporting.

    Args:
        exception: The exception to extract the chain from

    Returns:
        List of exception messages in the chain, from most specific to root cause
    """
    chain = [str(exception)]
    current = exception

    while hasattr(current, "__cause__") and current.__cause__:
        current = current.__cause__
        chain.append(str(current))

    return chain
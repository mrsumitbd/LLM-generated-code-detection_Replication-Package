from typing import Tuple
from enum import Enum

class ErrorCategory(Enum):
    NETWORK_ERROR = 1
    AUTHENTICATION_ERROR = 2
    INVALID_INPUT = 3
    INTERNAL_ERROR = 4
    UNKNOWN_ERROR = 5

def categorize_error(exception: Exception) -> Tuple[ErrorCategory, str]:
    """
    Categorize an exception to provide better user guidance.

    Args:
        exception: The exception to categorize

    Returns:
        Tuple of (ErrorCategory, suggestion) where suggestion is actionable advice
    """
    if isinstance(exception, ConnectionError):
        return ErrorCategory.NETWORK_ERROR, "Check your internet connection and try again."
    elif isinstance(exception, (ValueError, TypeError)):
        return ErrorCategory.INVALID_INPUT, "Please check your input and try again."
    elif isinstance(exception, (PermissionError, AuthenticationError)):
        return ErrorCategory.AUTHENTICATION_ERROR, "You may not have the necessary permissions. Please check your credentials and try again."
    else:
        return ErrorCategory.UNKNOWN_ERROR, "An unexpected error occurred. Please try again later or contact support."
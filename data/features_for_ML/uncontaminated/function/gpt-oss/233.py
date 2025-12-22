from typing import Tuple
from enum import Enum, auto

class ErrorCategory(Enum):
    """Simple error categories for user guidance."""
    VALUE_ERROR = auto()
    TYPE_ERROR = auto()
    FILE_ERROR = auto()
    NETWORK_ERROR = auto()
    AUTHENTICATION_ERROR = auto()
    UNKNOWN = auto()

def categorize_error(exception: Exception) -> Tuple[ErrorCategory, str]:
    """
    Categorize an exception to provide better user guidance.

    Args:
        exception: The exception to categorize

    Returns:
        Tuple of (ErrorCategory, suggestion) where suggestion is actionable advice
    """
    # Mapping of exception types to categories and suggestions
    if isinstance(exception, ValueError):
        return (
            ErrorCategory.VALUE_ERROR,
            "Check the values you provided; they may be out of the expected range or format."
        )
    if isinstance(exception, TypeError):
        return (
            ErrorCategory.TYPE_ERROR,
            "Verify that you are passing arguments of the correct type to the function."
        )
    if isinstance(exception, FileNotFoundError):
        return (
            ErrorCategory.FILE_ERROR,
            "Ensure the file path is correct and the file exists."
        )
    if isinstance(exception, PermissionError):
        return (
            ErrorCategory.FILE_ERROR,
            "Check file permissions; you may need read/write access."
        )
    if isinstance(exception, ConnectionError):
        return (
            ErrorCategory.NETWORK_ERROR,
            "Check your network connection and retry."
        )
    if isinstance(exception, TimeoutError):
        return (
            ErrorCategory.NETWORK_ERROR,
            "The operation timed out; try again or increase the timeout."
        )
    if isinstance(exception, OSError):
        return (
            ErrorCategory.FILE_ERROR,
            "An OS-level error occurred; check the error message for details."
        )
    if isinstance(exception, KeyError):
        return (
            ErrorCategory.VALUE_ERROR,
            "A required key is missing from a dictionary; verify the key name."
        )
    if isinstance(exception, AttributeError):
        return (
            ErrorCategory.VALUE_ERROR,
            "An object does not have the expected attribute; check the object's type."
        )
    if isinstance(exception, PermissionError):
        return (
            ErrorCategory.AUTHENTICATION_ERROR,
            "Authentication failed; verify credentials and permissions."
        )
    # Default case for unknown exceptions
    return (
        ErrorCategory.UNKNOWN,
        f"An unexpected error occurred: {exception!s}. Please consult the logs or contact support."
    )
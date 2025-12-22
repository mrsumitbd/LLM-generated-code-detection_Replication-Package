from typing import Tuple
from enum import Enum

class ErrorCategory(Enum):
    NETWORK = "network"
    PERMISSION = "permission"
    FILE_NOT_FOUND = "file_not_found"
    INVALID_INPUT = "invalid_input"
    TIMEOUT = "timeout"
    RESOURCE = "resource"
    UNKNOWN = "unknown"

def categorize_error(exception: Exception) -> Tuple[ErrorCategory, str]:
    """
    Categorize an exception to provide better user guidance.

    Args:
        exception: The exception to categorize

    Returns:
        Tuple of (ErrorCategory, suggestion) where suggestion is actionable advice
    """
    exception_type = type(exception).__name__
    exception_msg = str(exception).lower()
    
    # Network errors
    if isinstance(exception, (ConnectionError, TimeoutError, OSError)):
        if "timeout" in exception_msg or isinstance(exception, TimeoutError):
            return (ErrorCategory.TIMEOUT, "The operation timed out. Check your network connection or try again later.")
        return (ErrorCategory.NETWORK, "Network connection failed. Check your internet connection and try again.")
    
    if exception_type in ("URLError", "HTTPError", "ConnectionRefusedError", "ConnectionResetError"):
        return (ErrorCategory.NETWORK, "Unable to connect to the server. Verify the URL and network connectivity.")
    
    # Permission errors
    if isinstance(exception, PermissionError):
        return (ErrorCategory.PERMISSION, "You don't have permission to access this resource. Check file/directory permissions.")
    
    if exception_type == "PermissionDenied":
        return (ErrorCategory.PERMISSION, "Permission denied. Run with appropriate privileges or check access rights.")
    
    # File not found errors
    if isinstance(exception, FileNotFoundError):
        return (ErrorCategory.FILE_NOT_FOUND, "The specified file or directory was not found. Verify the path and try again.")
    
    if isinstance(exception, IsADirectoryError):
        return (ErrorCategory.FILE_NOT_FOUND, "Expected a file but found a directory. Check the path provided.")
    
    # Invalid input errors
    if isinstance(exception, (ValueError, TypeError, KeyError, IndexError)):
        return (ErrorCategory.INVALID_INPUT, "Invalid input provided. Check the format and type of your input data.")
    
    if isinstance(exception, AttributeError):
        return (ErrorCategory.INVALID_INPUT, "Attribute not found. Verify the object structure and attribute names.")
    
    if isinstance(exception, (json.JSONDecodeError if 'json' in dir() else type(None))):
        return (ErrorCategory.INVALID_INPUT, "Invalid JSON format. Check the syntax of your JSON data.")
    
    # Resource errors
    if isinstance(exception, (MemoryError, RecursionError)):
        return (ErrorCategory.RESOURCE, "Insufficient system resources. Try freeing up memory or simplifying the operation.")
    
    if isinstance(exception, OSError) and "No space left" in str(exception):
        return (ErrorCategory.RESOURCE, "No disk space available. Free up storage space and try again.")
    
    # Default to unknown
    return (ErrorCategory.UNKNOWN, f"An unexpected error occurred: {exception_msg}. Please check the error details and try again.")
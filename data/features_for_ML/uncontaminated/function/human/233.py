from typing import Any, Dict, List, Optional, Tuple, Union

def categorize_error(exception: Exception) -> Tuple[ErrorCategory, str]:
    """
    Categorize an exception to provide better user guidance.

    Args:
        exception: The exception to categorize

    Returns:
        Tuple of (ErrorCategory, suggestion) where suggestion is actionable advice
    """
    error_text = str(exception)
    root_cause = extract_root_cause(exception)

    # MSI-X specific errors (prioritize early for targeted guidance)
    lower_text = error_text.lower()
    lower_root = root_cause.lower()
    if (
        "msix" in lower_text
        or "msi-x" in lower_text
        or "msi x" in lower_text
        or "msix" in lower_root
    ):
        suggestion = _build_msix_suggestion(error_text)
        return (ErrorCategory.MSIX, suggestion)

    # File and permission related errors
    if (
        isinstance(exception, (FileNotFoundError, PermissionError))
        or "Permission denied" in root_cause
    ):
        return (
            ErrorCategory.PERMISSION,
            (
                "Check file permissions and ensure you have access to the "
                "required resources."
            ),
        )

    # Template related errors
    if (
        "Template" in error_text
        or "template" in error_text.lower()
        or "jinja" in error_text.lower()
    ):
        return (
            ErrorCategory.TEMPLATE,
            (
                "There's an issue with the template. Check the template syntax "
                "and ensure all required variables are provided."
            ),
        )

    # Configuration related errors
    if "config" in error_text.lower() or "configuration" in error_text.lower():
        return (
            ErrorCategory.CONFIGURATION,
            "Check your configuration settings and ensure they are valid.",
        )

    # Network related errors
    if (
        "network" in error_text.lower()
        or "connection" in error_text.lower()
        or "timeout" in error_text.lower()
    ):
        return (
            ErrorCategory.NETWORK,
            (
                "Check your network connection and ensure the target service "
                "is available."
            ),
        )

    # Resource related errors
    if "resource" in error_text.lower() or "not found" in error_text.lower():
        return (
            ErrorCategory.RESOURCE,
            "Ensure all required resources are available and properly configured.",
        )

    # Data related errors
    if (
        "data" in error_text.lower()
        or "parse" in error_text.lower()
        or "format" in error_text.lower()
    ):
        return (
            ErrorCategory.DATA,
            (
                "Check your data format and ensure it's valid according to the "
                "expected schema."
            ),
        )

    # Default to unknown
    return (
        ErrorCategory.UNKNOWN,
        "An unexpected error occurred. Check the logs for more details.",
    )
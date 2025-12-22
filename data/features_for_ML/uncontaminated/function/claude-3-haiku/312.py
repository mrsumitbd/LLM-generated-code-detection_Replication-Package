def _get_pages_selector(self) -> tuple[str, str]:
    """
    Get the pages selector for Cursor IDE.

    Returns:
        Tuple of (JS script, selector)
    """
    return (
        "return document.querySelectorAll('.page-item:not(.disabled) a.page-link')",
        ".page-item:not(.disabled) a.page-link",
    )
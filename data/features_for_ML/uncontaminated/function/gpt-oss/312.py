def _get_pages_selector(self) -> tuple[str, str]:
    """
    Get the pages selector for Cursor IDE.

    Returns:
        Tuple of (JS script, selector)
    """
    # JavaScript snippet that returns an array of page titles (or identifiers)
    js_script = (
        "return Array.from(document.querySelectorAll('div[data-testid=\"page\"]'))"
        ".map(el => el.textContent.trim());"
    )
    # CSS selector that matches page elements in the Cursor IDE UI
    selector = "div[data-testid='page']"
    return js_script, selector
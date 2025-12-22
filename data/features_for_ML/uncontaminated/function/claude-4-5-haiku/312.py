def _get_pages_selector(self) -> tuple[str, str]:
    """
    Get the pages selector for Cursor IDE.

    Returns:
        Tuple of (JS script, selector)
    """
    js_script = """
    (function() {
        const pages = document.querySelectorAll('[data-testid="page"]');
        return Array.from(pages).map((page, index) => ({
            index: index,
            title: page.getAttribute('data-title') || `Page ${index + 1}`,
            content: page.innerText
        }));
    })()
    """
    selector = '[data-testid="page"]'
    return (js_script, selector)
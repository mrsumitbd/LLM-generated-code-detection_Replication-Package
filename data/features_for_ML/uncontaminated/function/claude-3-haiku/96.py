def html_escape(s):
    """
    Escapes special characters in a string for use in HTML.

    Args:
        s (str): The input string to be escaped.

    Returns:
        str: The escaped string.
    """
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in s)
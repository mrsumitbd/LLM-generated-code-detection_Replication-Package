def html_escape(s):
    """
    Escape a string for safe inclusion in HTML.

    Replaces the following characters with their corresponding HTML entities:
        &  -> &amp;
        <  -> &lt;
        >  -> &gt;
        "  -> &quot;
        '  -> &#x27;   (or &apos; if preferred)

    Parameters
    ----------
    s : str
        The input string to escape.

    Returns
    -------
    str
        The escaped string.
    """
    if not isinstance(s, str):
        s = str(s)
    # Escape ampersand first to avoid double-escaping
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace("'", "&#x27;")
    return s
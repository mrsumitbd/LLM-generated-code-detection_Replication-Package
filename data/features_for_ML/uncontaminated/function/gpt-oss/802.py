import re

def extract_from_tag_block(txt: str, tag: str) -> str:
    """
    Extract the first occurrence of content inside a tag block.

    Parameters
    ----------
    txt : str
        The text to search.
    tag : str
        The tag name to look for (without angle brackets).

    Returns
    -------
    str
        The content inside the first matching <tag>...</tag> block.
        If no such block is found, returns an empty string.
    """
    # Build a regex that matches <tag ...> ... </tag>
    # \b ensures we match the tag name exactly
    # [^>]* allows for attributes in the opening tag
    # (.*?) captures the content lazily
    pattern = rf'<{re.escape(tag)}\b[^>]*>(.*?)</{re.escape(tag)}>'
    match = re.search(pattern, txt, flags=re.DOTALL)
    return match.group(1) if match else ''
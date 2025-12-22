from typing import Iterable, Any

def extract_text_blocks(blocks: Iterable[Any] | None) -> str:
    """
    Extracts textual content from an iterable of blocks.

    Parameters
    ----------
    blocks : Iterable[Any] | None
        An iterable containing block objects. Each block may be:
        - a string (used directly)
        - an object with a `text` attribute
        - a mapping (e.g., dict) with a `'text'` key
        - any other type (ignored)

    Returns
    -------
    str
        A single string containing all extracted text blocks joined by newlines.
        If `blocks` is None or empty, returns an empty string.
    """
    if not blocks:
        return ""

    texts = []
    for block in blocks:
        if block is None:
            continue
        # Direct string
        if isinstance(block, str):
            texts.append(block)
            continue
        # Mapping with 'text' key
        if isinstance(block, dict) and "text" in block:
            txt = block["text"]
            if isinstance(txt, str):
                texts.append(txt)
            continue
        # Object with 'text' attribute
        txt = getattr(block, "text", None)
        if isinstance(txt, str):
            texts.append(txt)

    return "\n".join(texts)
from typing import Any

def handle_url_response(response: Any) -> Any:
    """
    Convert a ParseResponse instance into a FullParseResponse instance.

    The function attempts to construct a FullParseResponse by unpacking the
    attributes of the given `response`.  If that fails (e.g. because the
    constructor signature does not match the attributes), it falls back to
    wrapping the original response in a FullParseResponse instance.

    Parameters
    ----------
    response : Any
        An instance of ParseResponse (or any object with a ``__dict__``).

    Returns
    -------
    Any
        An instance of FullParseResponse.
    """
    # Try to construct FullParseResponse by passing all attributes of response.
    try:
        return FullParseResponse(**response.__dict__)  # type: ignore
    except Exception:
        # Fallback: wrap the original response in a FullParseResponse.
        return FullParseResponse(response=response)  # type: ignore
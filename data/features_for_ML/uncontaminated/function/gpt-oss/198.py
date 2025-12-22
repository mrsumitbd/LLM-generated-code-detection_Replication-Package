from typing import Optional
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

def _add_claims_as_query_param(url: str, claims: Optional[dict[str, str]]) -> str:
    """
    Append the provided claims as query parameters to the given URL.

    Parameters
    ----------
    url : str
        The original URL.
    claims : Optional[dict[str, str]]
        A dictionary of claim key/value pairs to add as query parameters.
        If None or empty, the URL is returned unchanged.

    Returns
    -------
    str
        The URL with the claims appended as query parameters.
    """
    if not claims:
        return url

    # Parse the original URL
    parsed = urlparse(url)

    # Extract existing query parameters as a list of tuples
    existing_params = parse_qsl(parsed.query, keep_blank_values=True)

    # Append new claim parameters
    new_params = existing_params + list(claims.items())

    # Encode the combined parameters
    encoded_query = urlencode(new_params, doseq=True)

    # Reconstruct the URL with the new query string
    new_parsed = parsed._replace(query=encoded_query)
    return urlunparse(new_parsed)
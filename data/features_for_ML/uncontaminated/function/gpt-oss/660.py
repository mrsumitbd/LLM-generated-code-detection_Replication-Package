import uuid

def generate_uuid(ua_type: str) -> str:
    """
    Generate a UUID string based on the provided user agent type.

    Parameters
    ----------
    ua_type : str
        The user agent type string. If empty or None, a random UUID4 is returned.
        Otherwise, a deterministic UUID5 is generated using the DNS namespace.

    Returns
    -------
    str
        The generated UUID as a string.
    """
    if not ua_type:
        return str(uuid.uuid4())
    # Use a deterministic namespace (DNS) and the ua_type as the name
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, ua_type))
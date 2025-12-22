import re
from typing import List

def _split_camel_case(name: str) -> List[str]:
    """
    Split a camel‑case or PascalCase string into its constituent words.
    Example: "UserAddressStreet" -> ["User", "Address", "Street"]
    """
    # Insert space before each capital letter that follows a lower‑case letter or digit
    split = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', name)
    # Also split before capital letters that are followed by lower‑case letters
    split = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', split)
    return split.split()

def get_chained_entity_path(entity_name: str) -> str:
    """
    Convert an entity name into a chained path string.

    The function accepts an entity name that may be expressed in one of the
    following forms:
        * dotted notation: "User.Address.Street"
        * underscore notation: "user_address_street"
        * camel‑case or PascalCase: "UserAddressStreet"

    It normalises the name by:
        1. Splitting on dots, underscores, or camel‑case boundaries.
        2. Lower‑casing each component.
        3. Joining the components with a forward slash.

    Examples:
        >>> get_chained_entity_path("User.Address.Street")
        'user/address/street'
        >>> get_chained_entity_path("user_address_street")
        'user/address/street'
        >>> get_chained_entity_path("UserAddressStreet")
        'user/address/street'
        >>> get_chained_entity_path("SimpleEntity")
        'simpleentity'
    """
    if not entity_name:
        return ""

    # First split on dots or underscores
    parts = re.split(r'[._]', entity_name)

    # For each part, further split camel‑case segments
    split_parts = []
    for part in parts:
        if part:
            split_parts.extend(_split_camel_case(part))

    # Filter out empty strings and lower‑case the components
    cleaned = [p.lower() for p in split_parts if p]

    # Join with slashes
    return "/".join(cleaned)
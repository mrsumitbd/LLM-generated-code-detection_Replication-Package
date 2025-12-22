import re
from typing import Final

# Default suffix used for message entities
MESSAGES_SUFFIX: Final[str] = "_messages"

def _slugify(value: str) -> str:
    """Return a lowercase slugified version of the input string."""
    # Replace any non-alphanumeric character with an underscore
    return re.sub(r"\W+", "_", value.lower()).strip("_")

def get_contact_entity_id(
    domain: str,
    device_name: str,
    pubkey: str,
    suffix: str = MESSAGES_SUFFIX,
) -> str:
    """
    Create a consistent entity ID for contact entities.

    The entity ID is constructed from the domain, device name, and public key,
    with an optional suffix. All parts are slugified to ensure they contain
    only lowercase alphanumeric characters and underscores.

    Parameters
    ----------
    domain : str
        The domain of the entity (e.g., "contact").
    device_name : str
        The name of the device.
    pubkey : str
        The public key associated with the contact.
    suffix : str, optional
        A suffix to append to the entity ID. Defaults to MESSAGES_SUFFIX.

    Returns
    -------
    str
        A valid, consistent entity ID.
    """
    # Slugify each component to keep the ID safe
    domain_slug = _slugify(domain)
    device_slug = _slugify(device_name)
    pubkey_slug = _slugify(pubkey)

    # Construct the base ID
    base_id = f"{domain_slug}.{device_slug}_{pubkey_slug}"

    # Append the suffix if provided
    if suffix:
        suffix_slug = _slugify(suffix)
        entity_id = f"{base_id}{suffix_slug}"
    else:
        entity_id = base_id

    return entity_id
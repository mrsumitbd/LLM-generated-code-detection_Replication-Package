from .const import BAT_VMAX, BAT_VMIN, CHANNEL_PREFIX, DOMAIN, MESSAGES_SUFFIX, NodeType

def get_contact_entity_id(
    domain: str, device_name: str, pubkey: str, suffix: str = MESSAGES_SUFFIX
) -> str:
    """Create a consistent entity ID for contact entities."""
    return format_entity_id(domain, device_name, pubkey, suffix)
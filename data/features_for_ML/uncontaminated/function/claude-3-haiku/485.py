def get_contact_entity_id(
    domain: str, device_name: str, pubkey: str, suffix: str = MESSAGES_SUFFIX
) -> str:
    """Create a consistent entity ID for contact entities."""
    return f"{domain}:{device_name}:{pubkey}:{suffix}"
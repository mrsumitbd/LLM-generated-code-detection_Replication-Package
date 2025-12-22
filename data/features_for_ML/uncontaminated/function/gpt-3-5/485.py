def get_contact_entity_id(domain: str, device_name: str, pubkey: str, suffix: str = MESSAGES_SUFFIX) -> str:
    return f"{domain}-{device_name}-{pubkey}-{suffix}"
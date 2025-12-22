def get_contact_entity_id(
    domain: str, device_name: str, pubkey: str, suffix: str = MESSAGES_SUFFIX
) -> str:
    """Create a consistent entity ID for contact entities."""
    import hashlib
    
    # Create a unique identifier from the pubkey
    pubkey_hash = hashlib.sha256(pubkey.encode()).hexdigest()[:8]
    
    # Sanitize device_name to be safe for entity IDs
    sanitized_device_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in device_name.lower())
    
    # Combine components to create entity ID
    entity_id = f"{domain}_{sanitized_device_name}_{pubkey_hash}_{suffix}".lower()
    
    return entity_id
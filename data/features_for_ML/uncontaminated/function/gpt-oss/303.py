def verify_credentials(public_key_bytes):
    """
    Verify that the supplied bytes represent a valid public key.
    The function attempts to load the key as DER or PEM. If loading succeeds,
    the key is considered valid and the function returns True. Otherwise,
    it returns False.
    """
    try:
        # Try DER format first
        from cryptography.hazmat.primitives.serialization import load_der_public_key
        load_der_public_key(public_key_bytes)
        return True
    except Exception:
        try:
            # Try PEM format
            from cryptography.hazmat.primitives.serialization import load_pem_public_key
            load_pem_public_key(public_key_bytes)
            return True
        except Exception:
            return False
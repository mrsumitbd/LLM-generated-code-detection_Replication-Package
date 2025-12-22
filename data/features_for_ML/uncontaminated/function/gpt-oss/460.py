import base64
import json
from typing import Any, Dict, Optional

def _b64url_decode(data: str) -> bytes:
    """Decode a base64url-encoded string, adding padding if necessary."""
    # Replace URL-safe characters
    data = data.replace('-', '+').replace('_', '/')
    # Pad with '=' to make length a multiple of 4
    padding = 4 - (len(data) % 4)
    if padding and padding != 4:
        data += '=' * padding
    return base64.b64decode(data)

def decode_jws(jws: str) -> Optional[Dict[str, Any]]:
    """
    Decode the provided JWS payload.

    Returns:
        The decoded JWS payload as a dictionary, or None if decoding fails.
    """
    if not isinstance(jws, str):
        return None

    parts = jws.split('.')
    if len(parts) != 3:
        return None

    header_b64, payload_b64, signature_b64 = parts

    try:
        # Decode header (not used but validated)
        _b64url_decode(header_b64)
        # Decode payload
        payload_bytes = _b64url_decode(payload_b64)
        payload_str = payload_bytes.decode('utf-8')
        payload = json.loads(payload_str)
        if not isinstance(payload, dict):
            return None
        return payload
    except (ValueError, json.JSONDecodeError, base64.binascii.Error, UnicodeDecodeError):
        return None
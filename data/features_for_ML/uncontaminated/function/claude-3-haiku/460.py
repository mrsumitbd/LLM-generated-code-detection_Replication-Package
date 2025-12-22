import base64
import json
from typing import Dict, Any

def decode_jws(jws: str) -> Dict[str, Any] | None:
    """
    Decode the provided JWS payload.

    Returns:
        The decoded JWS payload as a dictionary.
    """
    try:
        parts = jws.split('.')
        if len(parts) != 3:
            return None

        payload_b64 = parts[1]
        payload_json = base64.b64decode(payload_b64 + '==').decode('utf-8')
        payload = json.loads(payload_json)
        return payload
    except (IndexError, base64.binascii.Error, json.JSONDecodeError):
        return None
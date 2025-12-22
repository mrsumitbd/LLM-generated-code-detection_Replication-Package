import json
import base64
from typing import Dict, Any

def decode_jws(jws: str) -> Dict[str, Any] | None:
    """
    Decode the provided JWS payload.

    Returns:
        The decoded JWS payload as a dictionary.
    """
    try:
        # Split the JWS into its three parts: header.payload.signature
        parts = jws.split('.')
        
        if len(parts) != 3:
            return None
        
        # Extract the payload (second part)
        payload = parts[1]
        
        # Add padding if necessary
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        # Decode the base64url encoded payload
        decoded_bytes = base64.urlsafe_b64decode(payload)
        
        # Parse the JSON
        decoded_payload = json.loads(decoded_bytes)
        
        return decoded_payload
    except (ValueError, IndexError, json.JSONDecodeError):
        return None
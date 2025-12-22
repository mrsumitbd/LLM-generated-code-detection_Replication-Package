import base64
from typing import Any, Dict
import json

def decode_jws(jws: str) -> Dict[str, Any] | None:
    """
    Decode the provided JWS payload.

    Returns:
        The decoded JWS payload as a dictionary.
    """
    try:
        parts: list[str] = jws.split(".")
        if len(parts) != 3:
            logger.debug(
                f"Decoding JWS failed: Invalid JWS format, expected 3 parts but got {len(parts)}: {jws}"
            )
            return None

        padded: str = parts[1] + "=" * (4 - len(parts[1]) % 4)
        decoded: bytes = base64.urlsafe_b64decode(padded)
        return json.loads(decoded)

    except Exception as e:
        logger.exception("Error decoding JWS token. Caused by, ", exc_info=e)
        return None
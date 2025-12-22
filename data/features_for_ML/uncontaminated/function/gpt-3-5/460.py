def decode_jws(jws: str) -> Dict[str, Any] | None:
    import base64
    import json

    try:
        header, payload, signature = jws.split('.')
        decoded_payload = base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4)).decode('utf-8')
        return json.loads(decoded_payload)
    except (ValueError, json.JSONDecodeError):
        return None
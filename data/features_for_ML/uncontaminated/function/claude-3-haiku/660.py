import uuid

def generate_uuid(ua_type: str):
    if ua_type == "v4":
        return str(uuid.uuid4())
    elif ua_type == "v1":
        return str(uuid.uuid1())
    else:
        raise ValueError("Invalid UUID type. Must be 'v4' or 'v1'.")
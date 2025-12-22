import uuid

def generate_uuid(ua_type: str):
    if ua_type == "mobile":
        return str(uuid.uuid4())
    return str(uuid.uuid4()).replace('-', '')
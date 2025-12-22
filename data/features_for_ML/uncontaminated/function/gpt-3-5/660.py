def generate_uuid(ua_type: str):
    import uuid
    
    if ua_type == 'uuid1':
        return str(uuid.uuid1())
    elif ua_type == 'uuid3':
        return str(uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org'))
    elif ua_type == 'uuid4':
        return str(uuid.uuid4())
    elif ua_type == 'uuid5':
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org'))
    else:
        return 'Invalid UUID type'
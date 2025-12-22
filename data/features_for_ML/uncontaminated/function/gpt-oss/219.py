import uuid

def generate_dynamic_class_name(base_name: str) -> str:
    return f"{base_name}_{uuid.uuid4().hex}"
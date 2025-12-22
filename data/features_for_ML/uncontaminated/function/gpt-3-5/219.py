def generate_dynamic_class_name(base_name: str) -> str:
    import uuid
    return f"{base_name}_{uuid.uuid4().hex[:8]}"
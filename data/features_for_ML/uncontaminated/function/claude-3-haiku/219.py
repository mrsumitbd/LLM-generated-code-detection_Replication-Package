def generate_dynamic_class_name(base_name: str) -> str:
    import random
    import string

    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{base_name}_{random_suffix}"
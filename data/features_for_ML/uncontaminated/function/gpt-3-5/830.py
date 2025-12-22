def create_error_message(error_type: ErrorType, message: str, component: str = "") -> str:
    return f"[{component}] [{error_type}] {message}"
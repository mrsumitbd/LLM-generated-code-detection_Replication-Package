def serialize_config(config):
    serialized_config = ""
    for key, value in config.items():
        serialized_config += f"{key}={value}\n"
    return serialized_config
def config_content(config):
    content = ""
    for key, value in config.items():
        content += f"{key}={value}\n"
    return content
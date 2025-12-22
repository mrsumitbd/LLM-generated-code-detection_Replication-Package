def config_content(config):
    try:
        with open(config, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return None
    except IOError:
        return None
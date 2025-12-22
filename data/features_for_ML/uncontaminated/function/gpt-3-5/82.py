def keep(conf):
    return {key: value for key, value in conf.items() if value is not None}
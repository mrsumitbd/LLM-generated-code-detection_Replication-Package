def computed_reactive(**computed_props):
    def decorator(cls):
        for prop_name, prop_func in computed_props.items():
            setattr(cls, prop_name, property(prop_func))
        return cls
    return decorator
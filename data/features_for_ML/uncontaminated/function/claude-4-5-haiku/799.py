def check_if_model_uses_unserializable_features(model: type[BaseModel]) -> None:
    """Validate a Pydantic model to determine if information will be lost when serializing.

    We cannot serialize the arbitrary python code in pydantic field/model validators, as well as
    the use of `default_factory` with an arbitrary callable. If the model contains usages of these,
    we can still serialize them, but these validators will not be included in the serialized form.
    """
    from pydantic import field_validator, model_validator
    from pydantic.fields import FieldInfo
    
    # Check for field validators
    for attr_name in dir(model):
        attr = getattr(model, attr_name, None)
        if attr is None:
            continue
        
        # Check if the attribute has validator markers
        if hasattr(attr, '__pydantic_validator__'):
            raise ValueError(
                f"Model {model.__name__} uses field validators which cannot be serialized. "
                f"Validator found on: {attr_name}"
            )
        
        if hasattr(attr, '__pydantic_model_validator__'):
            raise ValueError(
                f"Model {model.__name__} uses model validators which cannot be serialized. "
                f"Validator found on: {attr_name}"
            )
    
    # Check for default_factory in fields
    if hasattr(model, 'model_fields'):
        for field_name, field_info in model.model_fields.items():
            if isinstance(field_info, FieldInfo):
                if field_info.default_factory is not None:
                    # Check if it's a built-in or standard library callable
                    factory = field_info.default_factory
                    module = getattr(factory, '__module__', '')
                    
                    # Allow built-in types and standard library factories
                    if not (module.startswith('builtins') or 
                            module.startswith('typing') or
                            callable(factory) and factory in (list, dict, set, tuple)):
                        raise ValueError(
                            f"Model {model.__name__} uses default_factory with arbitrary callable "
                            f"on field '{field_name}' which cannot be serialized."
                        )
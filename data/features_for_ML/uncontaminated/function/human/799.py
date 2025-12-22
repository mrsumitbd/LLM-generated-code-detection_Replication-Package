from pydantic import BaseModel

def check_if_model_uses_unserializable_features(model: type[BaseModel]) -> None:
    """Validate a Pydantic model to determine if information will be lost when serializing.

    We cannot serialize the arbitrary python code in pydantic field/model validators, as well as
    the use of `default_factory` with an arbitrary callable. If the model contains usages of these,
    we can still serialize them, but these validators will not be included in the serialized form.
    """
    decorators = getattr(model, "__pydantic_decorators__", None)
    if decorators:
        has_field_validators = bool(getattr(decorators, "field_validators", None))
        has_model_validators = bool(getattr(decorators, "model_validators", None))
        if has_field_validators or has_model_validators:
            logger.warning("Field/Model validators are not supported for cloud execution and will be ignored.")

    fields = getattr(model, "model_fields", {})
    fields_with_default_factory = []
    fields_with_callable_default = []
    for f in fields.values():
        # Block callables in defaults
        if callable(getattr(f, "default_factory", None)):
            fields_with_default_factory.append(f)
        if callable(getattr(f, "default", None)):
            fields_with_callable_default.append(f)

    if fields_with_default_factory:
        logger.warning(f"Usage of `default_factory` in fields: {fields_with_default_factory} is not supported for "
                       f"cloud execution and will be ignored.")
    if fields_with_callable_default:
        logger.warning(f"Usage of `default` with a `Callable` or nested pydantic model in fields: "
                       f"{fields_with_callable_default} is not supported for cloud execution and will be ignored.")
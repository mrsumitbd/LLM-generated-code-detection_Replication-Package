from typing import Type
from pydantic.fields import FieldInfo, Validator
from pydantic.main import BaseModel

def check_if_model_uses_unserializable_features(model: Type[BaseModel]) -> None:
    """Validate a Pydantic model to determine if information will be lost when serializing.

    We cannot serialize the arbitrary python code in pydantic field/model validators, as well as
    the use of `default_factory` with an arbitrary callable. If the model contains usages of these,
    we can still serialize them, but these validators will not be included in the serialized form.
    """
    for field in model.__fields__.values():
        if any(isinstance(validator, Validator) and validator.is_complex for validator in field.validators):
            print(f"Field '{field.name}' has a complex validator that cannot be serialized.")
        if field.default_factory is not None and not isinstance(field.default_factory, type):
            print(f"Field '{field.name}' has a non-serializable default_factory.")
    for validator in model.__validators__.values():
        if validator.is_complex:
            print(f"Model '{model.__name__}' has a complex validator that cannot be serialized.")
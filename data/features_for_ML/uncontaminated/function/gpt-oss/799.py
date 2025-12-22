from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel

def check_if_model_uses_unserializable_features(model: type[BaseModel]) -> None:
    """
    Validate a Pydantic model to determine if information will be lost when serializing.

    We cannot serialize the arbitrary python code in pydantic field/model validators,
    as well as the use of `default_factory` with an arbitrary callable. If the model
    contains usages of these, we can still serialize them, but these validators will
    not be included in the serialized form.
    """
    # Check for default_factory usage
    for field_name, field in model.__fields__.items():
        if field.default_factory is not None:
            raise ValueError(
                f"Field `{field_name}` uses a default_factory which cannot be serialized."
            )

    # Check for validators usage
    # Pydantic v1 stores validators in `__validators__` (dict of field -> list of validators)
    # and root validators in `__root_validators__` (list of validators).
    # Pydantic v2 stores validators in `model.__validators__` (dict of name -> validator).
    # We consider any presence of validators as unserializable.
    validators_present = False

    # Pydantic v1
    if hasattr(model, "__validators__"):
        if model.__validators__:
            validators_present = True

    # Pydantic v2
    if hasattr(model, "__validators__"):
        if isinstance(model.__validators__, dict) and model.__validators__:
            validators_present = True

    # Root validators (v1)
    if hasattr(model, "__root_validators__"):
        if model.__root_validators__:
            validators_present = True

    if validators_present:
        raise ValueError(
            f"Model `{model.__name__}` contains validators which cannot be serialized."
        )
from typing import Any, Type
from django.db import models
import uuid

def parse_model_id(model: Type[models.Model], item_id: str) -> Any:
    """
    Converts a path parameter string to the correct type for the model's PK.
    Supports AutoField (int) and UUIDField (str).
    """
    pk_field = model._meta.pk

    # AutoField (or any IntegerField) -> int
    if isinstance(pk_field, models.AutoField) or isinstance(pk_field, models.IntegerField):
        try:
            return int(item_id)
        except ValueError as exc:
            raise ValueError(f"Invalid integer ID '{item_id}' for model {model.__name__}") from exc

    # UUIDField -> str (validate format)
    if isinstance(pk_field, models.UUIDField):
        try:
            # Validate UUID format; keep as string
            uuid.UUID(item_id)
        except ValueError as exc:
            raise ValueError(f"Invalid UUID ID '{item_id}' for model {model.__name__}") from exc
        return item_id

    # Unsupported PK type
    raise TypeError(
        f"Unsupported primary key type {type(pk_field).__name__} for model {model.__name__}"
    )
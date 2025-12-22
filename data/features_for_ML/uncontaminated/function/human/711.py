from typing import Any, Callable, Optional, Type, Dict
from django.db import models

def parse_model_id(model: Type[models.Model], item_id: str) -> Any:
    """
    Converts a path parameter string to the correct type for the model's PK.
    Supports AutoField (int) and UUIDField (str).
    """
    pk_field = model._meta.pk
    if isinstance(pk_field, models.AutoField) and item_id.isdigit():
        return int(item_id)
    return item_id
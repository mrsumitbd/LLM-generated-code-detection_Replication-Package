import uuid
from typing import Type, Any
from django.db import models


def parse_model_id(model: Type[models.Model], item_id: str) -> Any:
    """
    Converts a path parameter string to the correct type for the model's PK.
    Supports AutoField (int) and UUIDField (str).
    """
    pk_field = model._meta.pk
    
    if isinstance(pk_field, models.AutoField) or isinstance(pk_field, models.BigAutoField):
        return int(item_id)
    elif isinstance(pk_field, models.UUIDField):
        return uuid.UUID(item_id)
    else:
        return item_id
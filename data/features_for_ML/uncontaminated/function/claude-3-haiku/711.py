from typing import Any, Type
from django.db import models

def parse_model_id(model: Type[models.Model], item_id: str) -> Any:
    """
    Converts a path parameter string to the correct type for the model's PK.
    Supports AutoField (int) and UUIDField (str).
    """
    try:
        if issubclass(model, models.Model):
            if issubclass(model._meta.pk.__class__, models.AutoField):
                return int(item_id)
            elif issubclass(model._meta.pk.__class__, models.UUIDField):
                return item_id
            else:
                raise ValueError(f"Unsupported primary key type: {model._meta.pk.__class__}")
        else:
            raise ValueError("model must be a subclass of django.db.models.Model")
    except (ValueError, TypeError):
        raise ValueError(f"Invalid item_id: {item_id}")
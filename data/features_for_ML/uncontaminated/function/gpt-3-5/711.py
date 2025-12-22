def parse_model_id(model: Type[models.Model], item_id: str) -> Any:
    if isinstance(model._meta.pk, models.AutoField):
        return int(item_id)
    elif isinstance(model._meta.pk, models.UUIDField):
        return item_id
    else:
        raise ValueError("Unsupported primary key type for the model")
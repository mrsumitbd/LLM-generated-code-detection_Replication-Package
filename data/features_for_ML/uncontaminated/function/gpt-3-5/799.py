def check_if_model_uses_unserializable_features(model: type[BaseModel]) -> None:
    from pydantic import BaseModel

    def check_field(field):
        if field.field_info.extra.get('validators') or field.field_info.extra.get('default_factory'):
            print(f"Field '{field.name}' in model '{model.__name__}' uses unserializable features.")

    for field_name in model.__fields__:
        check_field(model.__fields__[field_name])
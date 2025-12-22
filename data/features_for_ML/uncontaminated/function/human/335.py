from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)
from dataclasses import MISSING, asdict, dataclass, field, fields, is_dataclass
from derisk._private import pydantic

def _get_base_model_descriptions(model_cls: "BaseModel") -> List[ParameterDescription]:
    from derisk._private import pydantic

    version = int(pydantic.VERSION.split(".")[0])  # type: ignore
    schema = model_cls.model_json_schema() if version >= 2 else model_cls.schema()
    required_fields = set(schema.get("required", []))
    param_descs = []
    for field_name, field_schema in schema.get("properties", {}).items():
        field = model_cls.model_fields[field_name]
        param_type = field_schema.get("type")
        if not param_type and "anyOf" in field_schema:
            for any_of in field_schema["anyOf"]:
                if any_of["type"] != "null":
                    param_type = any_of["type"]
                    break
        if version >= 2:
            default_value = (
                field.default
                if hasattr(field, "default")
                and str(field.default) != "PydanticUndefined"
                else None
            )
        else:
            default_value = (
                field.default
                if not field.allow_none
                else (
                    field.default_factory() if callable(field.default_factory) else None
                )
            )
        description = field_schema.get("description", "")
        is_required = field_name in required_fields
        valid_values = None
        ext_metadata = None
        if hasattr(field, "field_info"):
            valid_values = (
                list(field.field_info.choices)
                if hasattr(field.field_info, "choices")
                else None
            )
            ext_metadata = (
                field.field_info.extra if hasattr(field.field_info, "extra") else None
            )
        param_class = f"{model_cls.__module__}.{model_cls.__name__}"
        param_desc = ParameterDescription(
            param_class=param_class,
            param_name=field_name,
            param_type=param_type,
            default_value=default_value,
            description=description,
            required=is_required,
            valid_values=valid_values,
            ext_metadata=ext_metadata,
        )
        param_descs.append(param_desc)
    return param_descs
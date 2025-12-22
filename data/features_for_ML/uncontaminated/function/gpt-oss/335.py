from typing import List
from pydantic import BaseModel

# Assume ParameterDescription is defined elsewhere in the same package.
# Import it here. If it lives in a different module, adjust the import accordingly.
try:
    from .parameter_description import ParameterDescription
except Exception:  # pragma: no cover
    # Fallback: define a minimal stub for type checking purposes.
    class ParameterDescription:
        def __init__(self, name: str, type_: type, default: object = None, description: str | None = None):
            self.name = name
            self.type_ = type_
            self.default = default
            self.description = description

        def __repr__(self):
            return (
                f"ParameterDescription(name={self.name!r}, type_={self.type_!r}, "
                f"default={self.default!r}, description={self.description!r})"
            )


def _get_base_model_descriptions(model_cls: "BaseModel") -> List[ParameterDescription]:
    """
    Extract a list of ParameterDescription objects from a Pydantic BaseModel subclass.

    Parameters
    ----------
    model_cls : BaseModel
        The Pydantic model class to introspect.

    Returns
    -------
    List[ParameterDescription]
        A list of ParameterDescription instances, one for each field defined on the model.
    """
    if not issubclass(model_cls, BaseModel):
        raise TypeError("model_cls must be a subclass of pydantic.BaseModel")

    descriptions: List[ParameterDescription] = []

    # Pydantic stores field information in the __fields__ attribute.
    for field_name, field in model_cls.__fields__.items():
        # Resolve the actual type of the field.
        field_type = field.outer_type_

        # Determine the default value. Pydantic uses `None` for unset defaults,
        # but we want to preserve the original default if it exists.
        default_value = (
            field.default
            if field.default is not None
            else (
                field.default_factory()
                if field.default_factory is not None
                else None
            )
        )

        # Extract the description from FieldInfo if present.
        description_text = field.field_info.description

        descriptions.append(
            ParameterDescription(
                name=field_name,
                type_=field_type,
                default=default_value,
                description=description_text,
            )
        )

    return descriptions
from dataclasses import fields
from typing import List, Optional, Type

from .parameter_description import ParameterDescription

def _get_parameter_descriptions(
    dataclass_type: Type, parent_field: Optional[str] = None, **kwargs
) -> List[ParameterDescription]:
    parameter_descriptions = []
    for field in fields(dataclass_type):
        field_type = field.type
        if hasattr(field_type, '__dataclass_fields__'):
            nested_descriptions = _get_parameter_descriptions(
                field_type, parent_field=field.name, **kwargs
            )
            parameter_descriptions.extend(nested_descriptions)
        else:
            parameter_description = ParameterDescription(
                name=field.name,
                type=field_type,
                parent_field=parent_field,
                **kwargs
            )
            parameter_descriptions.append(parameter_description)
    return parameter_descriptions
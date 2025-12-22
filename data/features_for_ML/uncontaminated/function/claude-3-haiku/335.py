from typing import List
from pydantic import BaseModel

def _get_base_model_descriptions(model_cls: "BaseModel") -> List[ParameterDescription]:
    descriptions = []
    for field_name, field in model_cls.__fields__.items():
        description = ParameterDescription(
            name=field_name,
            type=field.type_,
            default=field.default,
            required=field.required,
            description=field.field_info.description,
        )
        descriptions.append(description)
    return descriptions

class ParameterDescription:
    def __init__(
        self,
        name: str,
        type: type,
        default: any,
        required: bool,
        description: str,
    ):
        self.name = name
        self.type = type
        self.default = default
        self.required = required
        self.description = description
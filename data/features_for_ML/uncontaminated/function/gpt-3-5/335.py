from typing import List

def _get_base_model_descriptions(model_cls: "BaseModel") -> List[ParameterDescription]:
    return model_cls.__init__.__annotations__.items()
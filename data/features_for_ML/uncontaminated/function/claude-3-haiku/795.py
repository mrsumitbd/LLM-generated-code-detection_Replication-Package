from typing import Callable, Dict, List, Tuple, Union
from dataclasses import dataclass, field
from inspect import signature, Parameter

@dataclass
class ParametersSchema:
    required: List[str] = field(default_factory=list)
    properties: Dict[str, Dict[str, Union[str, type]]] = field(default_factory=dict)

@dataclass
class FunctionSpec:
    name: str
    description: str
    parameters: ParametersSchema

def llm_function(func: Callable[P, R]) -> Callable[P, R]:
    sig = signature(func)
    params_schema = ParametersSchema()

    for param_name, param in sig.parameters.items():
        param_info = {
            "type": str(param.annotation) if param.annotation != Parameter.empty else "any",
            "description": param.description if param.description else ""
        }
        if param.default == Parameter.empty:
            params_schema.required.append(param_name)
        params_schema.properties[param_name] = param_info

    function_spec = FunctionSpec(
        name=func.__name__,
        description=func.__doc__.split("\n")[0] if func.__doc__ else "",
        parameters=params_schema
    )

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper._function_spec = function_spec
    return wrapper
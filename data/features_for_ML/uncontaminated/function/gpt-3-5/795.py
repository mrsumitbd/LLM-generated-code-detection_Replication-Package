from typing import Callable, TypeVar, get_type_hints
from inspect import signature
from dataclasses import dataclass
import json

P = TypeVar('P')
R = TypeVar('R')

@dataclass
class ParameterSpec:
    name: str
    type: str
    description: str
    required: bool

@dataclass
class ParametersSchema:
    parameters: list

    def to_dict(self):
        return {
            'type': 'object',
            'properties': {param.name: {'type': param.type} for param in self.parameters},
            'required': [param.name for param in self.parameters if param.required]
        }

@dataclass
class FunctionSpec:
    name: str
    description: str
    parameters: ParametersSchema

def llm_function(func: Callable[P, R]) -> Callable[P, R]:
    params = []
    for param_name, param in signature(func).parameters.items():
        param_type = param.annotation.__name__ if param.annotation != param.empty else 'Any'
        param_desc = func.__doc__.split(':param ' + param_name + ': ')[1].split('\n')[0] if ':param ' + param_name + ':' in func.__doc__ else ''
        param_required = param.default == param.empty
        params.append(ParameterSpec(param_name, param_type, param_desc, param_required))
    
    func_spec = FunctionSpec(func.__name__, func.__doc__.split('\n\n')[0], ParametersSchema(params))
    setattr(func, '_function_spec', func_spec)
    
    return func
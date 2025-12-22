import json
import ast

def deserialize(value: str | bytes, target_type: type[T], json: bool = False) -> T:
    if json:
        return target_type(json.loads(value))
    else:
        return target_type(ast.literal_eval(value))
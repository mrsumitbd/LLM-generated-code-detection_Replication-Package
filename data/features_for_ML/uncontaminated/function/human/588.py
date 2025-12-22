import ast
from parser.context import ParseContext
from parser.resolution.utils import resolve_call_signature

def handle_launch_config(node: ast.Call, context: ParseContext) -> dict:
    args, _ = resolve_call_signature(node, context.engine)
    if not args:
        raise ValueError("LaunchConfiguration must have a name.")

    name = args[0]
    context.introspection.track_launch_config_usage(name)

    return {"type": "LaunchConfiguration", "name": name}
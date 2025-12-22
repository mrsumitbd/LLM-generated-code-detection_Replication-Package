from fabric_cli.core import fab_constant, fab_logger
from fabric_cli.core.fab_exceptions import FabricCLIError

def validate_expression(expression: str, allowed_keys: list[str]) -> None:
    if not any(
        expression == key or expression.startswith(f"{key}.") for key in allowed_keys
    ):
        allowed_expressions = "\n  ".join(allowed_keys)
        raise FabricCLIError(
            f"Invalid query '{expression}'\n\nAvailable queries:\n  {allowed_expressions}",
            fab_constant.ERROR_INVALID_INPUT,
        )
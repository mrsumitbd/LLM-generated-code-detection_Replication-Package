from opentelemetry.context import get_value, attach, set_value

def get_chained_entity_path(entity_name: str) -> str:
    parent = get_value("entity_path")
    if parent is None:
        return entity_name
    else:
        return f"{parent}.{entity_name}"
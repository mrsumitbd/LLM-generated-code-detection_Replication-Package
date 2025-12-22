from typing import TYPE_CHECKING, Any

def get_middleware_info() -> dict[str, Any]:
    middleware_configs = _load_middleware_config()
    return {
        "config": middleware_configs,
        "applied_globally": _global_middleware_applied,
        "total_capabilities": len(_capabilities),
        "middleware_names": [m.get("name") for m in middleware_configs],
    }
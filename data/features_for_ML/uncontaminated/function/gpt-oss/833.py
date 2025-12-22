from collections import defaultdict
from typing import Dict, List, Any

def extract_categories_from_openapi(openapi_spec: dict) -> dict[str, list[dict]]:
    """
    Extract categories and their routes from OpenAPI spec.

    Args:
        openapi_spec: OpenAPI specification dictionary

    Returns:
        Dictionary mapping category names to lists of route info
    """
    categories: Dict[str, List[dict]] = defaultdict(list)

    paths = openapi_spec.get("paths", {})
    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            # Skip non-HTTP methods (e.g., parameters, summary)
            if method.lower() not in {"get", "post", "put", "delete", "patch", "options", "head", "trace"}:
                continue
            if not isinstance(operation, dict):
                continue

            tags = operation.get("tags", [])
            if not tags:
                tags = ["Uncategorized"]

            route_info = {
                "path": path,
                "method": method.upper(),
                "summary": operation.get("summary"),
                "operationId": operation.get("operationId"),
            }

            for tag in tags:
                categories[tag].append(route_info)

    return dict(categories)
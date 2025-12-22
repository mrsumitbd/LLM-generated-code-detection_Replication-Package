def extract_categories_from_openapi(openapi_spec: dict) -> dict[str, list[dict]]:
    """Extract categories and their routes from OpenAPI spec.

    Args:
        openapi_spec: OpenAPI specification dictionary

    Returns:
        Dictionary mapping category names to lists of route info
    """
    categories = {}

    if "paths" not in openapi_spec:
        return categories

    for path, methods in openapi_spec["paths"].items():
        for method, operation in methods.items():
            if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                tags = operation.get("tags", ["Uncategorized"])

                route_info = {
                    "path": path,
                    "method": method.upper(),
                    "operation_id": operation.get("operationId", ""),
                    "summary": operation.get("summary", ""),
                    "description": operation.get("description", ""),
                    "tags": tags,
                }

                for tag in tags:
                    if tag not in categories:
                        categories[tag] = []
                    categories[tag].append(route_info)

    return categories
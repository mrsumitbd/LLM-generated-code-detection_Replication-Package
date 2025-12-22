def extract_categories_from_openapi(openapi_spec: dict) -> dict[str, list[dict]]:
    """Extract categories and their routes from OpenAPI spec.

    Args:
        openapi_spec: OpenAPI specification dictionary

    Returns:
        Dictionary mapping category names to lists of route info
    """
    categories = {}

    for path, path_info in openapi_spec['paths'].items():
        for method, method_info in path_info.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch', 'options']:
                tags = method_info.get('tags', [])
                for tag in tags:
                    if tag not in categories:
                        categories[tag] = []
                    categories[tag].append({
                        'path': path,
                        'method': method.upper(),
                        'summary': method_info.get('summary', ''),
                        'description': method_info.get('description', ''),
                    })

    return categories
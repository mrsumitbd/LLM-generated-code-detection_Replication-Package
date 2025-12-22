def extract_categories_from_openapi(openapi_spec: dict) -> dict[str, list[dict]]:
    categories = {}
    paths = openapi_spec.get('paths', {})
    
    for path, path_info in paths.items():
        category = path.split('/')[1]
        if category not in categories:
            categories[category] = []
        
        route_info = {
            'path': path,
            'methods': list(path_info.keys())
        }
        categories[category].append(route_info)
    
    return categories
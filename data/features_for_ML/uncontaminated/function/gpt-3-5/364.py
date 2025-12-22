def _find_collection_response(op: Operation) -> Tuple[int, Any]:
    for status_code, response in op.responses.items():
        if response.content:
            for media_type, media_type_obj in response.content.items():
                if 'application/json' in media_type:
                    if 'schema' in media_type_obj:
                        schema = media_type_obj['schema']
                        if schema.get('type') == 'array':
                            items = schema.get('items')
                            if items and 'type' in items:
                                return status_code, items
    return 0, None
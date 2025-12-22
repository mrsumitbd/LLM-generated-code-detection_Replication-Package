def wrapper(model):
            try:
                field_values = {}
                for field in fields:
                    if hasattr(model, field):
                        field_values[field] = getattr(model, field)

                if not constraint_func(**field_values):
                    return error_message or f"Cross-field constraint failed for fields: {', '.join(fields)}"
                return None
            except Exception as e:
                return f"Cross-field constraint error: {str(e)}"
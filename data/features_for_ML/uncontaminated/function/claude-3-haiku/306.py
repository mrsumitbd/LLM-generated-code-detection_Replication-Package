def _format_index(index: sqlalchemy.engine.interfaces.ReflectedIndex) -> str:
    index_name = index.name
    columns = [col.name for col in index.columns]
    unique = "UNIQUE " if index.unique else ""
    return f"{unique}INDEX {index_name} ({', '.join(columns)})"
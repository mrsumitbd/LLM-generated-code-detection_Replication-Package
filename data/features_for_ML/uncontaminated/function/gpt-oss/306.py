from sqlalchemy.engine.interfaces import ReflectedIndex

def _format_index(index: ReflectedIndex) -> str:
    """
    Return a human‑readable representation of a reflected index.

    The format is:
        [UNIQUE] INDEX <index_name> (<col1>, <col2>, ...)

    Parameters
    ----------
    index : ReflectedIndex
        The reflected index object from SQLAlchemy.

    Returns
    -------
    str
        A formatted string describing the index.
    """
    # Build the prefix: UNIQUE (if applicable) + INDEX
    parts = []
    if getattr(index, "unique", False):
        parts.append("UNIQUE")
    parts.append("INDEX")

    # Index name
    parts.append(index.name)

    # Column list
    # `index.columns` is an iterable of Column objects; use their `name` attribute.
    col_names = ", ".join(col.name for col in getattr(index, "columns", []))
    parts.append(f"({col_names})")

    return " ".join(parts)
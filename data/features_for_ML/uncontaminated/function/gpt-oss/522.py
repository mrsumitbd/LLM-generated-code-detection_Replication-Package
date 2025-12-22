def _list_providers(providers: list[ModelProvider]):
    """
    Return a formatted string listing the available providers.

    Each provider is expected to have at least the attributes `id` and `name`.
    The output is a simple table with two columns: Provider ID and Provider Name.
    """
    if not providers:
        return "No providers available."

    # Determine column widths
    id_header = "Provider ID"
    name_header = "Provider Name"
    id_width = max(len(id_header), *(len(str(p.id)) for p in providers))
    name_width = max(len(name_header), *(len(str(p.name)) for p in providers))

    # Build header
    header = f"{id_header:<{id_width}}  {name_header:<{name_width}}"
    separator = f"{'-' * id_width}  {'-' * name_width}"

    # Build rows
    rows = []
    for p in providers:
        rows.append(f"{str(p.id):<{id_width}}  {str(p.name):<{name_width}}")

    # Combine all parts
    return "\n".join([header, separator] + rows)
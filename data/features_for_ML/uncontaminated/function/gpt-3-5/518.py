def format_name(project: NormalizedName, extras: FrozenSet[NormalizedName]) -> str:
    return f"{project} - {' - '.join(str(extra) for extra in extras)}"
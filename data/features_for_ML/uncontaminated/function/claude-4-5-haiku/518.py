def format_name(project: NormalizedName, extras: FrozenSet[NormalizedName]) -> str:
    if not extras:
        return str(project)
    
    sorted_extras = sorted(extras)
    extras_str = ",".join(sorted_extras)
    return f"{project}[{extras_str}]"
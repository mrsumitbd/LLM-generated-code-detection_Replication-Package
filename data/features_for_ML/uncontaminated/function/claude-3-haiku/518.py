def format_name(project: NormalizedName, extras: FrozenSet[NormalizedName]) -> str:
    project_name = project.name
    extras_names = ', '.join(extra.name for extra in extras)
    if extras_names:
        return f"{project_name} ({extras_names})"
    else:
        return project_name
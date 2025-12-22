def asset_creation_strategy() -> str:
    """Defines the preferred strategy for creating assets in Blender"""
    return (
        "Prefer creating assets as linked libraries or collections, "
        "using Blender's Asset Browser for easy reuse. "
        "Keep geometry data in separate .blend files, "
        "and reference them via library overrides or linked groups. "
        "This approach ensures modularity, version control, and efficient memory usage."
    )
def create_project_map(state: _State) -> dict:
    """
    Build a mapping from project identifiers to the corresponding project objects.

    The function is intentionally tolerant of different shapes of `state`:
    * If `state` has a `projects` attribute that is iterable, it is used.
    * If `state` behaves like a mapping and contains a `'projects'` key, that value is used.
    * If `state` is already a mapping of identifiers to project objects, it is returned unchanged.
    * If no projects can be found, an empty dictionary is returned.

    Projects are expected to expose an `id` attribute; if that is missing the project
    is skipped.  The resulting dictionary maps the project id to the project instance.
    """
    # If state is already a mapping of id -> project, just return it
    if isinstance(state, dict):
        # Heuristic: if keys look like ids (int/str) and values have an `id` attribute,
        # we assume it's already a project map.
        if all(
            (isinstance(k, (int, str)) and hasattr(v, "id") and v.id == k)
            for k, v in state.items()
        ):
            return state

    # Try to obtain an iterable of projects
    projects_iter = None
    if hasattr(state, "projects"):
        projects_iter = getattr(state, "projects")
    else:
        try:
            projects_iter = state.get("projects")
        except Exception:
            projects_iter = None

    # If we still don't have an iterable, default to empty list
    if projects_iter is None:
        projects_iter = []

    # Build the map
    project_map = {}
    for proj in projects_iter:
        # Skip if no id attribute
        if not hasattr(proj, "id"):
            continue
        project_map[proj.id] = proj

    return project_map
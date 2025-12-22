def create_project_map(state: _State) -> dict:
    project_map = {}
    for project in state.projects:
        project_map[project.id] = project.name
    return project_map
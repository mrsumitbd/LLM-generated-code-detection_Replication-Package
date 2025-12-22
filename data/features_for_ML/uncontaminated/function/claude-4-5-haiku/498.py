def create_project_map(state: _State) -> dict:
    """Create a mapping of project names to their configurations."""
    project_map = {}
    
    if hasattr(state, 'projects') and state.projects:
        for project in state.projects:
            if hasattr(project, 'name'):
                project_map[project.name] = project
    
    return project_map
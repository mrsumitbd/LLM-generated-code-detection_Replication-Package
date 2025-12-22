from deep_next.core.steps.gather_project_knowledge.project_map import tree

def create_project_map(state: _State) -> dict:
        project_map = tree(path=state.root_path)

        return {"project_map": project_map}
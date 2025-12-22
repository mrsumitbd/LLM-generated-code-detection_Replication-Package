class Resource:
    def __init__(self, name: str):
        self.name = name
        self.dependencies = []
        self.dependents = []

    def add_dependency(self, resource: 'Resource'):
        self.dependencies.append(resource)
        resource.dependents.append(self)

    def remove_dependency(self, resource: 'Resource'):
        self.dependencies.remove(resource)
        resource.dependents.remove(self)

    def get_dependencies(self) -> list['Resource']:
        return self.dependencies

    def get_dependents(self) -> list['Resource']:
        return self.dependents
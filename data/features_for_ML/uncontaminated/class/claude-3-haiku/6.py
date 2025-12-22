class ComputedBindingConfig:
    """Configuration for computed reactive bindings"""

    def __init__(self, expression, dependencies=None, name=None, description=None):
        self.expression = expression
        self.dependencies = dependencies or []
        self.name = name
        self.description = description

    def __repr__(self):
        return f"ComputedBindingConfig(expression={self.expression!r}, dependencies={self.dependencies!r}, name={self.name!r}, description={self.description!r})"

    def __eq__(self, other):
        if not isinstance(other, ComputedBindingConfig):
            return NotImplemented
        return (
            self.expression == other.expression
            and self.dependencies == other.dependencies
            and self.name == other.name
            and self.description == other.description
        )

    def __hash__(self):
        return hash((self.expression, tuple(self.dependencies), self.name, self.description))
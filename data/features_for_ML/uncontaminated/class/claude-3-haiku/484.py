class ToolDefinition:
    """Tool definition with metadata"""

    def __init__(self, name, description, version, author, license):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.license = license

    def __str__(self):
        return f"{self.name} v{self.version} by {self.author} ({self.license})"

    def __repr__(self):
        return f"ToolDefinition(name='{self.name}', description='{self.description}', version='{self.version}', author='{self.author}', license='{self.license}')"

    def __eq__(self, other):
        if isinstance(other, ToolDefinition):
            return (self.name == other.name and
                    self.description == other.description and
                    self.version == other.version and
                    self.author == other.author and
                    self.license == other.license)
        return False

    def __hash__(self):
        return hash((self.name, self.description, self.version, self.author, self.license))
class ComplianceRequirement:
    """Individual compliance requirement."""

    def __init__(self, name, description, category, priority):
        self.name = name
        self.description = description
        self.category = category
        self.priority = priority
        self.is_met = False

    def mark_as_met(self):
        self.is_met = True

    def mark_as_not_met(self):
        self.is_met = False

    def __str__(self):
        return f"{self.name} ({self.category}, Priority: {self.priority})"

    def __repr__(self):
        return f"ComplianceRequirement('{self.name}', '{self.description}', '{self.category}', {self.priority})"
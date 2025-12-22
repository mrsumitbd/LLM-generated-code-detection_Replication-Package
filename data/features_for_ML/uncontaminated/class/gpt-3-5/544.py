class ComplianceRequirement:
    def __init__(self, name, description, due_date):
        self.name = name
        self.description = description
        self.due_date = due_date

    def display_requirement(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Due Date: {self.due_date}")
class ToolDefinition:
    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Category: {self.category}")

# Example usage
tool1 = ToolDefinition("Hammer", "A tool used for driving nails", "Hand Tools")
tool1.display_info()
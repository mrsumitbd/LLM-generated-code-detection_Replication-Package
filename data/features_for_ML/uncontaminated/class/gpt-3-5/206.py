class BatchAction:
    """Represents a batch action for a NEAR promise."""

    def __init__(self):
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def execute(self):
        for action in self.actions:
            action.execute()

class Action:
    def __init__(self, name):
        self.name = name

    def execute(self):
        print(f"Executing action: {self.name}")

# Example usage:
batch = BatchAction()
action1 = Action("Action 1")
action2 = Action("Action 2")

batch.add_action(action1)
batch.add_action(action2)

batch.execute()
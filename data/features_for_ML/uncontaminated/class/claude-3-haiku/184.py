class Command:
    def __init__(self, _text, _id):
        self.text = _text
        self.id = _id

    def execute(self):
        print(f"Executing command: {self.text} (ID: {self.id})")

    def undo(self):
        print(f"Undoing command: {self.text} (ID: {self.id})")
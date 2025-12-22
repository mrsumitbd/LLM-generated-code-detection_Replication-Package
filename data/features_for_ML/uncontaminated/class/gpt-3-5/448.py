class BehavioralRegister:
    """Definition of a behavioral register."""

    def __init__(self):
        self.data = {}

    def to_dict(self) -> Dict[str, Any]:
        return self.data

# Example usage:
# register = BehavioralRegister()
# register.data = {'name': 'Alice', 'age': 30}
# print(register.to_dict())
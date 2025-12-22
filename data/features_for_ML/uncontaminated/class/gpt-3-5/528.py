class MockCompletion:
    
    def __init__(self):
        self.completed = False

    def complete(self):
        self.completed = True

    def is_completed(self):
        return self.completed

# Example usage:
mock = MockCompletion()
print(mock.is_completed())  # Output: False
mock.complete()
print(mock.is_completed())  # Output: True
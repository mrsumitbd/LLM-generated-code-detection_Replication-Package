class MessageValidator:
    
    def __init__(self):
        self.valid_messages = []

    def add_valid_message(self, message):
        self.valid_messages.append(message)

    def is_message_valid(self, message):
        return message in self.valid_messages

# Example usage:
# validator = MessageValidator()
# validator.add_valid_message("hello")
# validator.add_valid_message("world")
# print(validator.is_message_valid("hello"))  # Output: True
# print(validator.is_message_valid("python"))  # Output: False
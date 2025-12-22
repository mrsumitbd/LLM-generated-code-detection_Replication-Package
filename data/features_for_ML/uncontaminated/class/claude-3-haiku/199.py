class MessageValidator:
    def __init__(self):
        self.allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
        self.max_length = 140

    def validate_message(self, message):
        if len(message) > self.max_length:
            return False

        for char in message:
            if char not in self.allowed_characters:
                return False

        return True
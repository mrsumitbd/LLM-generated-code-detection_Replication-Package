class Chat:
    def __init__(self, client):
        self.client = client
        self.messages = []

    def send_message(self, message):
        self.client.send_message(message)
        self.messages.append(message)

    def receive_message(self):
        message = self.client.receive_message()
        self.messages.append(message)
        return message

    def get_chat_history(self):
        return self.messages
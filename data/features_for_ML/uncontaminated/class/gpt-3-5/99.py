class Chat:

    def __init__(self, client):
        self.client = client

    def send_message(self, message):
        print(f"Sending message: {message}")

    def receive_message(self, message):
        print(f"Received message: {message}")

# Example usage:
client = "Alice"
chat = Chat(client)
chat.send_message("Hello, Bob!")
chat.receive_message("Hi, Alice!")
class Chat:

    def __init__(self, client):
        self.client = client
        self.messages = []
        self.conversation_history = []

    def add_message(self, role, content):
        """Add a message to the chat history."""
        message = {"role": role, "content": content}
        self.messages.append(message)
        self.conversation_history.append(message)
        return message

    def get_messages(self):
        """Get all messages in the current chat."""
        return self.messages

    def clear_messages(self):
        """Clear all messages from the current chat."""
        self.messages = []

    def get_conversation_history(self):
        """Get the full conversation history."""
        return self.conversation_history

    def send_message(self, content):
        """Send a user message and get a response."""
        self.add_message("user", content)
        response = self.client.create_message(self.messages)
        if response:
            assistant_message = response.get("content", "")
            self.add_message("assistant", assistant_message)
            return assistant_message
        return None

    def reset(self):
        """Reset the chat to initial state."""
        self.messages = []
        self.conversation_history = []

    def __str__(self):
        """String representation of the chat."""
        return f"Chat with {len(self.messages)} messages"

    def __repr__(self):
        """Representation of the chat."""
        return f"Chat(client={self.client}, messages={len(self.messages)})"
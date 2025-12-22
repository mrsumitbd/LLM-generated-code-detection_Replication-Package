import anthropic


class Floor:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.client = anthropic.Anthropic()
        self.conversation_history = []

    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def chat(self, user_message):
        """Send a message and get a response from Claude."""
        self.add_message("user", user_message)
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are a helpful assistant. You are standing on a floor at coordinates ({}, {}). Answer questions helpfully and concisely.".format(self.x, self.y),
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.add_message("assistant", assistant_message)
        
        return assistant_message

    def get_position(self):
        """Get the current position on the floor."""
        return (self.x, self.y)

    def move(self, dx, dy):
        """Move to a new position on the floor."""
        self.x += dx
        self.y += dy
        return self.get_position()

    def reset_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def get_conversation_history(self):
        """Get the full conversation history."""
        return self.conversation_history
from anthropic import Anthropic
from typing import Any, Dict

client = Anthropic()

class UpdateRoleRequest:
    """update Role request object"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdateRoleRequest":
        return cls(**data)


def main():
    """Main function to demonstrate the UpdateRoleRequest class."""
    conversation_history = []
    
    system_prompt = """You are a helpful assistant that can help users understand and work with the UpdateRoleRequest class.
    The UpdateRoleRequest class is used to create update role request objects from dictionaries.
    You can help users create instances, understand the structure, and work with the class."""
    
    print("UpdateRoleRequest Assistant")
    print("=" * 50)
    print("This assistant helps you work with the UpdateRoleRequest class.")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8096,
            system=system_prompt,
            messages=conversation_history
        )
        
        assistant_message = response.content[0].text
        
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        print(f"\nAssistant: {assistant_message}\n")


if __name__ == "__main__":
    main()
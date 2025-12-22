import logging
import sys
from anthropic import Anthropic

def setup_logger():
    """Set up a logger for the application."""
    logger = logging.getLogger("multi_turn_conversation")
    logger.setLevel(logging.DEBUG)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


def main():
    """Main function to run the multi-turn conversation."""
    logger = setup_logger()
    client = Anthropic()
    conversation_history = []
    
    logger.info("Starting multi-turn conversation with Claude")
    print("Multi-turn Conversation with Claude")
    print("=" * 50)
    print("Type 'quit' to exit the conversation.\n")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            logger.info("User ended the conversation")
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        logger.debug(f"User message: {user_input}")
        
        # Send message to Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8096,
            system="You are a helpful assistant engaged in a multi-turn conversation. Provide clear, concise, and helpful responses.",
            messages=conversation_history
        )
        
        # Extract assistant's response
        assistant_message = response.content[0].text
        
        # Add assistant's response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        logger.debug(f"Assistant response: {assistant_message}")
        
        # Display the response
        print(f"\nAssistant: {assistant_message}\n")


if __name__ == "__main__":
    main()
import os
from anthropic import Anthropic

class ChromeConfig:
    """Configuration for Chrome driver."""
    
    def __init__(self):
        """Initialize ChromeConfig with default settings."""
        self.headless = True
        self.window_size = (1920, 1080)
        self.user_agent = None
        self.proxy = None
        self.disable_images = False
        self.disable_javascript = False
        self.timeout = 30
        self.additional_args = []
        self.client = Anthropic()
        self.conversation_history = []
    
    def set_headless(self, headless: bool) -> 'ChromeConfig':
        """Set headless mode."""
        self.headless = headless
        return self
    
    def set_window_size(self, width: int, height: int) -> 'ChromeConfig':
        """Set window size."""
        self.window_size = (width, height)
        return self
    
    def set_user_agent(self, user_agent: str) -> 'ChromeConfig':
        """Set custom user agent."""
        self.user_agent = user_agent
        return self
    
    def set_proxy(self, proxy: str) -> 'ChromeConfig':
        """Set proxy server."""
        self.proxy = proxy
        return self
    
    def disable_images(self) -> 'ChromeConfig':
        """Disable image loading."""
        self.disable_images = True
        return self
    
    def disable_javascript(self) -> 'ChromeConfig':
        """Disable JavaScript execution."""
        self.disable_javascript = True
        return self
    
    def set_timeout(self, timeout: int) -> 'ChromeConfig':
        """Set timeout in seconds."""
        self.timeout = timeout
        return self
    
    def add_argument(self, argument: str) -> 'ChromeConfig':
        """Add additional Chrome argument."""
        self.additional_args.append(argument)
        return self
    
    def get_chrome_options(self) -> dict:
        """Get Chrome options as dictionary."""
        options = {
            'headless': self.headless,
            'window_size': self.window_size,
            'timeout': self.timeout,
            'additional_args': self.additional_args
        }
        
        if self.user_agent:
            options['user_agent'] = self.user_agent
        
        if self.proxy:
            options['proxy'] = self.proxy
        
        if self.disable_images:
            options['disable_images'] = True
        
        if self.disable_javascript:
            options['disable_javascript'] = True
        
        return options
    
    def chat(self, user_message: str) -> str:
        """Send a message and get a response using Claude."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8096,
            system="You are a helpful assistant for configuring Chrome browser settings. Help users understand and configure Chrome options.",
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def reset_conversation(self) -> None:
        """Reset conversation history."""
        self.conversation_history = []
    
    def __repr__(self) -> str:
        """String representation of ChromeConfig."""
        return f"ChromeConfig({self.get_chrome_options()})"


def main():
    """Main function to demonstrate ChromeConfig usage."""
    config = ChromeConfig()
    
    # Configure Chrome settings
    config.set_headless(True).set_window_size(1280, 720).set_timeout(60)
    
    print("Chrome Configuration:")
    print(config)
    print()
    
    # Interactive chat with Claude about Chrome configuration
    print("Chat with Claude about Chrome configuration:")
    print("-" * 50)
    
    # Example conversation
    user_input = "What are the benefits of running Chrome in headless mode?"
    print(f"User: {user_input}")
    response = config.chat(user_input)
    print(f"Assistant: {response}")
    print()
    
    user_input = "How can I disable JavaScript in Chrome for testing purposes?"
    print(f"User: {user_input}")
    response = config.chat(user_input)
    print(f"Assistant: {response}")
    print()
    
    # Reset and start new conversation
    config.reset_conversation()
    print("Conversation reset.")


if __name__ == "__main__":
    main()
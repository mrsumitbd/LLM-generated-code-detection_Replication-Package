import threading
import queue
from anthropic import Anthropic

class BackgroundService:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.task_queue = queue.Queue()
        self.running = False
        self.thread = None
        self.client = Anthropic()
        self.conversation_history = []

    def add_task(self, task_func, *args, **kwargs):
        self.task_queue.put((task_func, args, kwargs))

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._process_tasks, daemon=True)
            self.thread.start()

    def _process_tasks(self):
        while self.running:
            try:
                task_func, args, kwargs = self.task_queue.get(timeout=1)
                task_func(*args, **kwargs)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing task: {e}")

    def chat(self, user_message):
        """Send a message and get a response from Claude."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system="You are a helpful assistant running in a background service. Keep responses concise and helpful.",
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message

    def stop(self):
        """Stop the background service."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)


def main():
    # Get the singleton instance
    service = BackgroundService.get_instance()
    
    # Start the background service
    service.start()
    
    # Define a task that uses the chat functionality
    def chat_task(message):
        print(f"User: {message}")
        response = service.chat(message)
        print(f"Assistant: {response}\n")
    
    # Add tasks to the queue
    service.add_task(chat_task, "What is the capital of France?")
    service.add_task(chat_task, "Tell me about its history.")
    service.add_task(chat_task, "What are some famous landmarks there?")
    
    # Wait for tasks to complete
    import time
    time.sleep(5)
    
    # Stop the service
    service.stop()
    print("Background service stopped.")


if __name__ == "__main__":
    main()
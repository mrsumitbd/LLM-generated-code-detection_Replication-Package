from anthropic import Anthropic

class Select:
    def __init__(self, *args):
        self.client = Anthropic()
        self.conversation_history = []
        self.items = list(args)
        self.selected_items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            
    def select(self, item):
        if item in self.items and item not in self.selected_items:
            self.selected_items.append(item)
            
    def deselect(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)
            
    def get_selected(self):
        return self.selected_items
    
    def get_items(self):
        return self.items
    
    def chat(self, user_message):
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        system_prompt = f"""You are a helpful assistant managing a selection interface.
Current items available: {self.items}
Currently selected items: {self.selected_items}

You can help users:
1. Select items from the available list
2. Deselect items from the selected list
3. View available items
4. View selected items
5. Add new items
6. Remove items

When the user wants to select or deselect items, respond with clear instructions.
Format your responses to be helpful and concise."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def clear_history(self):
        self.conversation_history = []
class WebhookEvent:
    """Standardized webhook event structure."""
    
    def __init__(self, event_type, event_data):
        self.event_type = event_type
        self.event_data = event_data
        
    def get_event_type(self):
        return self.event_type
    
    def get_event_data(self):
        return self.event_data
    
    def set_event_type(self, event_type):
        self.event_type = event_type
        
    def set_event_data(self, event_data):
        self.event_data = event_data
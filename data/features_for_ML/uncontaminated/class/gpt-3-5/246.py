class EventCfg:
    """Configuration for events."""
    
    def __init__(self, event_name, event_date, event_location):
        self.event_name = event_name
        self.event_date = event_date
        self.event_location = event_location
        
    def display_event_info(self):
        print(f"Event Name: {self.event_name}")
        print(f"Event Date: {self.event_date}")
        print(f"Event Location: {self.event_location}")
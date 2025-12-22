class AIRAState:
    """State object for AIRA LangGraph workflow."""
    
    def __init__(self, state_id, state_name, state_data):
        self.state_id = state_id
        self.state_name = state_name
        self.state_data = state_data
        
    def get_state_id(self):
        return self.state_id
    
    def get_state_name(self):
        return self.state_name
    
    def get_state_data(self):
        return self.state_data
    
    def set_state_id(self, state_id):
        self.state_id = state_id
        
    def set_state_name(self, state_name):
        self.state_name = state_name
        
    def set_state_data(self, state_data):
        self.state_data = state_data
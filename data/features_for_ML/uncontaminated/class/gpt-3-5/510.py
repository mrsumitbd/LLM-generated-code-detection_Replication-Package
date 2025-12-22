class ChromeConfig:
    """Configuration for Chrome driver."""
    
    def __init__(self, driver_path, headless=False, user_agent=None):
        self.driver_path = driver_path
        self.headless = headless
        self.user_agent = user_agent
        
    def set_driver_path(self, driver_path):
        self.driver_path = driver_path
        
    def set_headless(self, headless):
        self.headless = headless
        
    def set_user_agent(self, user_agent):
        self.user_agent = user_agent
        
    def get_driver_path(self):
        return self.driver_path
    
    def is_headless(self):
        return self.headless
    
    def get_user_agent(self):
        return self.user_agent
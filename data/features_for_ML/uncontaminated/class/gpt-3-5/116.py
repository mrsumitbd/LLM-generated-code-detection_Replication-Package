class Driver:
    
    def __init__(self, browser_config=None, *args, **kwargs):
        self.browser_config = browser_config
        self.closed = False
        self.context = None
        self.page = None

    def is_closed(self):
        return self.closed

    def get_context(self):
        return self.context

    def get_page(self):
        return self.page
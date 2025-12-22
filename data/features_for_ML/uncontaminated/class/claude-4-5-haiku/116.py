class Driver:

    def __init__(self, browser_config=None, *args, **kwargs):
        self.browser_config = browser_config or {}
        self.context = None
        self.page = None
        self.browser = None
        self._closed = True

    def is_closed(self):
        return self._closed

    def get_context(self):
        return self.context

    def get_page(self):
        return self.page
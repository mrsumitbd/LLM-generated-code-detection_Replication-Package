class Driver:
    def __init__(self, browser_config=None, *args, **kwargs):
        self.browser_config = browser_config
        self.driver = self._create_driver()

    def _create_driver(self):
        # Implement the logic to create a web driver based on the browser_config
        pass

    def is_closed(self):
        # Implement the logic to check if the web driver is closed
        return self.driver.session_id is None

    def get_context(self):
        # Implement the logic to get the current context of the web driver
        return self.driver.current_context

    def get_page(self):
        # Implement the logic to get the current page of the web driver
        return self.driver.current_url
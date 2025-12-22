class CheckForUpdate:
    """
        this class will handle the update availability, usefull for other script that use the sendemail, or for people that wanna build theyr own update logic. Also can be used internally
    """

    def __init__(self):
        self.current_version = None
        self.latest_version = None
        self.update_available = False
        self.update_message = None

    def parse_as_resp(self, response):
        """
        Parses the response from the update check and sets the class attributes accordingly.
        """
        try:
            self.current_version = response['current_version']
            self.latest_version = response['latest_version']
            self.update_available = self.current_version < self.latest_version
            self.update_message = response['update_message']
        except (KeyError, TypeError):
            self.update_available = False
            self.update_message = "Error parsing update response."

    def parse_as_output(self):
        """
        Returns a formatted string with the update information.
        """
        if self.update_available:
            return f"Update available! Current version: {self.current_version}, Latest version: {self.latest_version}\n{self.update_message}"
        else:
            return "No update available."
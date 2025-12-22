class CheckForUpdate:
    """
        this class will handle the update availability, usefull for other script that use the sendemail, or for people that wanna build theyr own update logic. Also can be used internally
    """      

    def __init__(self):
        self.current_version = None
        self.latest_version = None
        self.update_available = False
        self.release_notes = None
        self.download_url = None
        self.error = None

    def parse_as_resp(self):
        """
        Parse update information as a response object
        Returns a dictionary with update status and details
        """
        if self.error:
            return {
                "status": "error",
                "message": self.error,
                "update_available": False
            }
        
        return {
            "status": "success",
            "current_version": self.current_version,
            "latest_version": self.latest_version,
            "update_available": self.update_available,
            "release_notes": self.release_notes,
            "download_url": self.download_url
        }

    def parse_as_output(self):
        """
        Parse update information as formatted output string
        Returns a human-readable string representation
        """
        if self.error:
            return f"Error checking for updates: {self.error}"
        
        output = f"Current Version: {self.current_version}\n"
        output += f"Latest Version: {self.latest_version}\n"
        
        if self.update_available:
            output += "Status: Update Available!\n"
            if self.download_url:
                output += f"Download URL: {self.download_url}\n"
            if self.release_notes:
                output += f"Release Notes:\n{self.release_notes}\n"
        else:
            output += "Status: You are up to date.\n"
        
        return output
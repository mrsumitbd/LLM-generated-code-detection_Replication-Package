class RequestLogEntry:
    def __init__(self, timestamp, endpoint, status_code):
        self.timestamp = timestamp
        self.endpoint = endpoint
        self.status_code = status_code

    def __str__(self):
        return f"Timestamp: {self.timestamp}, Endpoint: {self.endpoint}, Status Code: {self.status_code}"
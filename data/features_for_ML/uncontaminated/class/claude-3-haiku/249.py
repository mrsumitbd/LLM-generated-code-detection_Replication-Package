class RequestLogEntry:
    """Container for request log information"""

    def __init__(self, request_id, timestamp, method, url, status_code, response_time):
        self.request_id = request_id
        self.timestamp = timestamp
        self.method = method
        self.url = url
        self.status_code = status_code
        self.response_time = response_time

    def __str__(self):
        return f"RequestLogEntry(request_id={self.request_id}, timestamp={self.timestamp}, method={self.method}, url={self.url}, status_code={self.status_code}, response_time={self.response_time})"

    def __repr__(self):
        return str(self)
class WebhookEvent:
    """Standardized webhook event structure."""

    def __init__(self, event_type, event_id, timestamp, data):
        self.event_type = event_type
        self.event_id = event_id
        self.timestamp = timestamp
        self.data = data

    def __str__(self):
        return f"WebhookEvent(event_type='{self.event_type}', event_id='{self.event_id}', timestamp='{self.timestamp}', data={self.data})"

    def __repr__(self):
        return str(self)
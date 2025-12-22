class CachedMeeting:
    """Cached meeting information with expiration."""
    
    def __init__(self, meeting_id, meeting_data, ttl=3600):
        """
        Initialize a cached meeting.
        
        Args:
            meeting_id: Unique identifier for the meeting
            meeting_data: Dictionary containing meeting information
            ttl: Time to live in seconds (default: 3600)
        """
        self.meeting_id = meeting_id
        self.meeting_data = meeting_data
        self.ttl = ttl
        self.created_at = self._get_current_time()
    
    def _get_current_time(self):
        """Get current time in seconds since epoch."""
        import time
        return time.time()
    
    def is_expired(self):
        """Check if the cached meeting has expired."""
        import time
        current_time = time.time()
        return (current_time - self.created_at) > self.ttl
    
    def get_data(self):
        """
        Get meeting data if not expired.
        
        Returns:
            Meeting data if valid, None if expired
        """
        if self.is_expired():
            return None
        return self.meeting_data
    
    def refresh(self, meeting_data=None):
        """
        Refresh the cache by updating timestamp and optionally data.
        
        Args:
            meeting_data: Optional new meeting data to update
        """
        self.created_at = self._get_current_time()
        if meeting_data is not None:
            self.meeting_data = meeting_data
    
    def update_ttl(self, new_ttl):
        """
        Update the time to live for this cached meeting.
        
        Args:
            new_ttl: New TTL in seconds
        """
        self.ttl = new_ttl
    
    def __repr__(self):
        """String representation of the cached meeting."""
        return f"CachedMeeting(id={self.meeting_id}, expired={self.is_expired()})"
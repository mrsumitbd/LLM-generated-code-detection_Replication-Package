from typing import Dict, List, Optional, Any, Tuple

class CachedMeeting:
    """Cached meeting information with expiration."""
    
    # Meeting basic info
    subject: str
    organizer: str
    start_time: str  # ISO format for JSON serialization
    end_time: str
    location: str
    
    # Attendee info
    attendees: List[Dict[str, str]]
    attendee_count: int
    
    # Display formatting
    display_text: str
    
    # Cache metadata
    cached_at: str  # When this was cached
    expires_at: str  # When this expires
    confidence_score: float
    
    # Rich meeting data for future UI
    body_preview: str = ""
    meeting_url: str = ""
    is_recurring: bool = False
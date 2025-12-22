from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

class MeetingInfo:
    """Meeting information extracted from calendar events."""
    
    # Basic meeting details
    id: str
    subject: str
    organizer_name: str
    organizer_email: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    
    # Attendees information
    attendees: List[Dict[str, str]] = None  # [{"name": "John Doe", "email": "john@example.com", "status": "accepted"}]
    required_attendees: List[str] = None    # List of required attendee emails
    optional_attendees: List[str] = None    # List of optional attendee emails
    
    # Meeting content
    body_preview: Optional[str] = None      # First 200 chars of meeting body
    body_html: Optional[str] = None         # Full HTML body (for agenda extraction)
    
    # Meeting metadata
    is_cancelled: bool = False
    is_all_day: bool = False
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    meeting_url: Optional[str] = None       # Teams/Zoom/etc. links
    
    # Correlation metadata
    confidence_score: float = 0.0          # How confident we are in the correlation (0.0 - 1.0)
    correlation_method: str = "manual"      # "timestamp", "manual", "ml" etc.
    
    def __post_init__(self):
        """Initialize default values for mutable fields."""
        if self.attendees is None:
            self.attendees = []
        if self.required_attendees is None:
            self.required_attendees = []
        if self.optional_attendees is None:
            self.optional_attendees = []
    
    @property
    def duration_minutes(self) -> int:
        """Calculate meeting duration in minutes."""
        return int((self.end_time - self.start_time).total_seconds() / 60)
    
    @property
    def attendee_count(self) -> int:
        """Get total number of attendees."""
        return len(self.attendees)
    
    @property
    def display_attendees(self) -> str:
        """Get formatted attendee list for display."""
        if not self.attendees:
            return "No attendees"
        
        names = [att.get("name", att.get("email", "Unknown")) for att in self.attendees[:3]]
        if len(self.attendees) > 3:
            names.append(f"and {len(self.attendees) - 3} more")
        return ", ".join(names)
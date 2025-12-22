from datetime import datetime
from typing import Dict, List, Optional, Any

class AudioMetadata:
    """Complete metadata for an audio recording."""
    
    # File identification
    filename: str
    file_path: str
    file_size: int
    duration_seconds: float
    date_created: datetime
    
    # Processing status
    processing_status: ProcessingStatus
    processing_started_at: Optional[datetime] = None
    processing_completed_at: Optional[datetime] = None
    processing_error: Optional[str] = None
    
    # Transcription data
    transcription_text: Optional[str] = None
    transcription_confidence: Optional[float] = None
    transcription_language: Optional[str] = None
    
    # AI-generated analysis
    ai_summary: Optional[str] = None
    ai_participants: Optional[List[str]] = None
    ai_action_items: Optional[List[str]] = None
    ai_topics: Optional[List[str]] = None
    ai_sentiment: Optional[str] = None
    ai_key_quotes: Optional[List[str]] = None
    
    # User-editable fields (can override AI)
    user_title: Optional[str] = None
    user_description: Optional[str] = None
    user_participants: Optional[List[str]] = None
    user_action_items: Optional[List[str]] = None
    user_tags: Optional[List[str]] = None
    user_notes: Optional[str] = None
    
    # Display fields (computed from above)
    display_title: Optional[str] = None  # user_title or ai_summary or filename
    display_description: Optional[str] = None  # user_description or ai_summary
    
    # Metadata
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
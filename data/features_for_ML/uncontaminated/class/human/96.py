from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

class SyncEvent:
    """同步事件记录"""
    timestamp: datetime
    account_id: str
    sync_type: str  # 'full' or 'incremental'
    status: str  # 'success', 'failed', 'partial'
    emails_synced: int = 0
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
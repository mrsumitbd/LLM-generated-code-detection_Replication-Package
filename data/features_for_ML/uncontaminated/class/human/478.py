import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from catzilla import Catzilla, service, Depends, JSONResponse, Path

class DatabaseService:
    """Database service (singleton scope)"""

    def __init__(self, config: DatabaseConfig = Depends("db_config")):
        self.config = config
        self.connection_id = str(uuid.uuid4())[:8]
        self.query_count = 0
        self.connected_at = datetime.now()

        print(f"💾 Database service created (singleton) - Connection: {self.connection_id}")

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute a database query"""
        self.query_count += 1
        return {
            "query": query,
            "connection_id": self.connection_id,
            "query_number": self.query_count,
            "executed_at": datetime.now().isoformat()
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            "connection_id": self.connection_id,
            "total_queries": self.query_count,
            "uptime": (datetime.now() - self.connected_at).total_seconds(),
            "config": {
                "host": self.config.host,
                "database": self.config.database
            }
        }
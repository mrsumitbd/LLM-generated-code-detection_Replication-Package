class DatabaseService:
    """Database service (singleton scope)"""

    def __init__(self, config: DatabaseConfig = Depends("db_config")):
        self.config = config
        self.connection = None
        self.query_count = 0
        self.error_count = 0
        self._connect()

    def _connect(self) -> None:
        """Establish database connection"""
        try:
            import sqlite3
            self.connection = sqlite3.connect(
                self.config.database_url or ":memory:",
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row
        except Exception as e:
            self.error_count += 1
            raise ConnectionError(f"Failed to connect to database: {str(e)}")

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute a database query and return results"""
        try:
            if not self.connection:
                self._connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
                self.query_count += 1
                return {
                    "success": True,
                    "data": results,
                    "row_count": len(results)
                }
            else:
                self.connection.commit()
                self.query_count += 1
                return {
                    "success": True,
                    "rows_affected": cursor.rowcount,
                    "data": None
                }
        except Exception as e:
            self.error_count += 1
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get database service statistics"""
        return {
            "query_count": self.query_count,
            "error_count": self.error_count,
            "database_url": self.config.database_url,
            "is_connected": self.connection is not None,
            "total_operations": self.query_count + self.error_count
        }
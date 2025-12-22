class DBConn:

    def __init__(self, db_service: DBService):
        self.db_service = db_service
        self.connection = None

    def connect(self):
        self.connection = self.db_service.get_connection()
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_sql(self, sql):
        if not self.connection:
            raise RuntimeError("Database connection not established. Call connect() first.")
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            self.connection.commit()
            return cursor.fetchall()
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()
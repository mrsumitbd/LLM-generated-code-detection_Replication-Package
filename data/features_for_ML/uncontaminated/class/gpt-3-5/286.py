class DBConn:

    def __init__(self, db_service: DBService):
        self.db_service = db_service
        self.connection = None

    def connect(self):
        self.connection = self.db_service.connect()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_sql(self, sql):
        if not self.connection:
            raise Exception("Connection is not established. Call connect() first.")
        
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
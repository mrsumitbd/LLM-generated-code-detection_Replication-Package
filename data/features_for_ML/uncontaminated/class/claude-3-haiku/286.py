class DBConn:
    def __init__(self, db_service: DBService):
        self.db_service = db_service
        self.connection = None

    def connect(self):
        self.connection = self.db_service.create_connection()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_sql(self, sql):
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
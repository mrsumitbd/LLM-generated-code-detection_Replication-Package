import json
import pymysql
import psycopg2
import pyodbc

class DBConn:
    def __init__(self, db_service: DBService):
        self.dbtype = db_service.db_type
        self.host = db_service.host
        self.port = db_service.port
        self.user = db_service.user
        self.password = db_service.password
        self.database = db_service.database
        self.conn = None

    def connect(self):
        if self.conn is not None:
            return

        if self.dbtype == 'mysql':
            self.conn = pymysql.connect(
                host=self.host, port=self.port,
                user=self.user, password=self.password,
                db=self.database, charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        elif self.dbtype == 'postgresql' or self.dbtype == 'pg':
            import psycopg2
            self.conn = psycopg2.connect(
                host=self.host, port=self.port,
                user=self.user, password=self.password,
                dbname=self.database
            )
        elif self.dbtype == 'sqlserver':
            import pyodbc
            driver = 'ODBC Driver 17 for SQL Server'
            conn_str = (
                f'DRIVER={{{driver}}};SERVER={self.host},{self.port};'
                f'UID={self.user};PWD={self.password};DATABASE={self.database}'
            )
            self.conn = pyodbc.connect(conn_str)
        else:
            raise ValueError('Unsupported dbtype')

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception as e:
                print(e)
            self.conn = None

    def execute_sql(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        if self.dbtype == 'mysql':
            result = [dict(row) for row in rows]
        elif self.dbtype == 'postgresql' or self.dbtype == 'pg':
            result = [dict(zip(columns, row)) for row in rows]
        elif self.dbtype == 'sqlserver':
            result = [dict(zip(columns, row)) for row in rows]
        else:
            result = []
        cursor.close()
        try:
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return str(result)
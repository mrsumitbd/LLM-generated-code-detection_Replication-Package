import os
from testcontainers.core.config import testcontainers_config
from testcontainers.postgres import PostgresContainer

class DbPostgresql:
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "postgres"
    POSTGRES_DBNAME = "postgres"
    POSTGRES_IMAGE = "debezium/example-postgres:3.0.0.Final"
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT_DEFAULT = 5432
    CONTAINER: PostgresContainer = (PostgresContainer(image=POSTGRES_IMAGE,
                                                      port=POSTGRES_PORT_DEFAULT,
                                                      username=POSTGRES_USER,
                                                      password=POSTGRES_PASSWORD,
                                                      dbname=POSTGRES_DBNAME,
                                                      )
                                    .with_exposed_ports(POSTGRES_PORT_DEFAULT)
                                    )
    PostgresContainer._connect = wait_for_postgresql_to_start

    def clean_files(self):
        if OFFSET_FILE.exists():
            os.remove(OFFSET_FILE)
        if DUCKDB_FILE.exists():
            os.remove(DUCKDB_FILE)

    def start(self):
        testcontainers_config.ryuk_disabled = True
        self.clean_files()
        print("Starting Postgresql Db...")
        self.CONTAINER.start()

    def stop(self):
        print("Stopping Postgresql Db...")
        self.CONTAINER.stop()
        self.clean_files()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
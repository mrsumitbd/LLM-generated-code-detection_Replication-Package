class DbPostgresql:

    def clean_files(self):
        print("Cleaning PostgreSQL files")

    def start(self):
        print("Starting PostgreSQL")

    def stop(self):
        print("Stopping PostgreSQL")

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting PostgreSQL")
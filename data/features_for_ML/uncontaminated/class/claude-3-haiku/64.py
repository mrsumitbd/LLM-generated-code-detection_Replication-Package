import subprocess
import os

class DbPostgresql:
    def __init__(self, db_name, db_user, db_password):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.process = None

    def clean_files(self):
        subprocess.run(["sudo", "rm", "-rf", "/var/lib/postgresql/data/*"])

    def start(self):
        self.process = subprocess.Popen(
            ["sudo", "-u", "postgres", "postgres", "-D", "/var/lib/postgresql/data"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def stop(self):
        self.process.terminate()
        self.process.wait()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
        self.clean_files()
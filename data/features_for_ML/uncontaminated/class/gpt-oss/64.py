import os
import shutil
import subprocess
from contextlib import contextmanager


class DbPostgresql:
    def __init__(
        self,
        name: str = "postgres_test",
        port: int = 5432,
        user: str = "postgres",
        password: str = "postgres",
        db: str = "postgres",
        data_dir: str | None = None,
    ):
        self.name = name
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.data_dir = data_dir or f"/tmp/{self.name}_data"
        self.container_running = False

    def clean_files(self):
        """Remove the data directory used by the PostgreSQL container."""
        if os.path.isdir(self.data_dir):
            shutil.rmtree(self.data_dir)

    def start(self):
        """Start a PostgreSQL Docker container."""
        os.makedirs(self.data_dir, exist_ok=True)

        # Build the docker run command
        cmd = [
            "docker",
            "run",
            "--name",
            self.name,
            "-e",
            f"POSTGRES_USER={self.user}",
            "-e",
            f"POSTGRES_PASSWORD={self.password}",
            "-e",
            f"POSTGRES_DB={self.db}",
            "-p",
            f"{self.port}:5432",
            "-v",
            f"{self.data_dir}:/var/lib/postgresql/data",
            "-d",
            "postgres:13",
        ]

        # Execute the command
        subprocess.run(cmd, check=True)
        self.container_running = True

    def stop(self):
        """Stop and remove the PostgreSQL Docker container."""
        if self.container_running:
            subprocess.run(["docker", "stop", self.name], check=True)
            subprocess.run(["docker", "rm", self.name], check=True)
            self.container_running = False

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure the container is stopped and data cleaned up."""
        self.stop()
        self.clean_files()
        return False
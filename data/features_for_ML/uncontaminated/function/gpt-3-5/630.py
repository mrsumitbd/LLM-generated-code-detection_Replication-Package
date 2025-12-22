from typing import Iterator

def download_db_from_docker(container_id: str, env: Env) -> Iterator[str]:
    # Get the database file self.sqlite_database from the running container using docker API.
    pass
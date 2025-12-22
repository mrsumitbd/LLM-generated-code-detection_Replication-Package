import docker
from typing import Iterator

def download_db_from_docker(container_id: str, env: Env) -> Iterator[str]:
    client = docker.from_env()
    container = client.containers.get(container_id)
    stream, _ = container.get_archive('/app/self.sqlite_database')
    for chunk in stream:
        yield chunk
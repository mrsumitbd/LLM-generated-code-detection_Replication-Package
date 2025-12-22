from docker import APIClient
from pathlib import Path

def write_to_container(container: Container, data: str, dst: Path):
    client = APIClient(base_url='unix://var/run/docker.sock')
    exec_id = client.exec_create(container=container.id, cmd=['sh', '-c', f'echo "{data}" > {dst}'])['Id']
    output = client.exec_start(exec_id)
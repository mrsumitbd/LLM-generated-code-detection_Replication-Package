import os
from pathlib import Path

def write_to_container(container: Container, data: str, dst: Path):
    """
    Write a string to a file in a docker container
    """
    container.exec_run(f"mkdir -p {dst.parent}")
    container.exec_run(f"echo '{data}' > {dst}")
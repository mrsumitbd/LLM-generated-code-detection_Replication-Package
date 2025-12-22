import docker
from pathlib import Path
from docker.types import Container

def copy_to_container(container: Container, src: Path, dst: Path):
    """
    Copy a file from local to a docker container

    Args:
        container (Container): Docker container to copy to
        src (Path): Source file path
        dst (Path): Destination file path in the container
    """
    src = Path(src)
    dst = Path(dst)
    
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")
    
    if src.is_file():
        with open(src, 'rb') as f:
            data = f.read()
        container.put_archive(str(dst.parent), data)
    else:
        raise ValueError(f"Source path is not a file: {src}")
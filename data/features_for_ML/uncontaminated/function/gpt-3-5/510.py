from docker import APIClient

def copy_to_container(container: Container, src: Path, dst: Path):
    client = APIClient()
    with open(src, 'rb') as f:
        data = f.read()
    client.put_archive(container.id, dst, data)
import docker
from typing import Union, List, Dict, Tuple

Container = docker.models.containers.Container

def run(
    image: str,
    command: List[str],
    volumes: Dict[str, str] | None = None,
    device_requests: List[Union[int, str]] | None = None,
    environment: Dict[str, str] | None = None,
    network: str | None = None,
    detach: bool = False,
    remove: bool = False,
    ports: Dict[str, str] | None = None,
    stdout: bool = True,
    stderr: bool = False,
    user: str | None = None,
    extra_args: List[str] | None = None,
) -> Union[Container, Tuple[bytes, bytes], bytes]:
    client = docker.from_env()

    container_kwargs = {
        "image": image,
        "command": command,
        "volumes": volumes,
        "device_requests": device_requests,
        "environment": environment,
        "network": network,
        "detach": detach,
        "remove": remove,
        "ports": ports,
        "user": user,
        "extra_hosts": extra_args,
    }

    container = client.containers.run(**container_kwargs)

    if detach:
        return container

    stdout_bytes, stderr_bytes = container.wait(timeout=None, stream=True)
    container.remove()

    if stdout and stderr:
        return stdout_bytes, stderr_bytes
    elif stdout:
        return stdout_bytes
    elif stderr:
        return stderr_bytes
    else:
        return b""
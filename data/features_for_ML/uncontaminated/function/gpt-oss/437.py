from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Import only for type checking; the actual runtime import is optional
    from docker.models.containers import Container

def write_to_container(container: "Container", data: str, dst: Path) -> None:
    """
    Write a string to a file in a docker container.

    Parameters
    ----------
    container : docker.models.containers.Container
        The Docker container instance.
    data : str
        The string content to write.
    dst : pathlib.Path
        The destination file path inside the container.

    Notes
    -----
    This function uses the Docker SDK's exec API to run a shell command
    that writes the data to the specified file. It streams the data
    through the container's stdin.
    """
    # Ensure dst is a string path
    dst_path = str(dst)

    # Build the command that will receive data from stdin and write it to dst
    # Using single quotes around the command to avoid shell expansion issues
    cmd = f"sh -c 'cat > {dst_path}'"

    # Execute the command with a socket to stream data
    # stdin=True allows us to send data to the container's stdin
    # socket=True returns a socket object we can write to
    sock = container.exec_run(cmd, socket=True, stdin=True)

    try:
        # Send the data as bytes
        sock.sendall(data.encode("utf-8"))
    finally:
        # Close the socket to signal EOF to the container
        sock.close()

    # Optionally, we could check the exit status of the exec command.
    # The Docker SDK does not provide the exit code directly when using
    # socket=True, so we rely on the container not raising an exception.
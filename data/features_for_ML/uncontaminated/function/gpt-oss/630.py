import os
import tarfile
import tempfile
from typing import Iterator

import docker

def download_db_from_docker(container_id: str, env) -> Iterator[str]:
    """
    Retrieve the SQLite database file from a running Docker container and yield its
    contents line by line.

    Parameters
    ----------
    container_id : str
        The ID or name of the running container.
    env : object
        An object that must expose a ``sqlite_database`` attribute containing the
        absolute path to the database file inside the container.

    Yields
    ------
    str
        Lines of the database file decoded as UTF‑8. Binary data will be decoded
        with ``errors='ignore'``.
    """
    # Ensure the env object has the required attribute
    if not hasattr(env, "sqlite_database"):
        raise AttributeError("The env object must have a 'sqlite_database' attribute")

    db_path_in_container = env.sqlite_database

    # Create a Docker client
    client = docker.from_env()

    # Get the container object
    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound as exc:
        raise RuntimeError(f"Container '{container_id}' not found") from exc

    # Retrieve the archive of the database file
    try:
        stream, stat = container.get_archive(db_path_in_container)
    except docker.errors.APIError as exc:
        raise RuntimeError(f"Failed to get archive for '{db_path_in_container}'") from exc

    # Write the tar stream to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tar_file:
        for chunk in stream:
            tar_file.write(chunk)
        tar_file_path = tar_file.name

    # Extract the database file from the tar archive
    with tarfile.open(tar_file_path, mode="r:*") as tar:
        # Find the member that matches the database file name
        members = [m for m in tar.getmembers() if m.name.endswith(os.path.basename(db_path_in_container))]
        if not members:
            raise RuntimeError(f"Database file '{db_path_in_container}' not found in the archive")
        member = members[0]
        extracted_path = os.path.join(tempfile.gettempdir(), member.name)
        tar.extract(member, path=tempfile.gettempdir())

    # Yield the file contents line by line
    try:
        with open(extracted_path, "rb") as f:
            for line in f:
                # Decode each line; ignore errors for binary data
                yield line.decode("utf-8", errors="ignore")
    finally:
        # Clean up temporary files
        try:
            os.remove(tar_file_path)
        except OSError:
            pass
        try:
            os.remove(extracted_path)
        except OSError:
            pass
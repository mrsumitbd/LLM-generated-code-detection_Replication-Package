import tarfile
import io
from pathlib import Path
from typing import Union

def copy_to_container(container: "Container", src: Union[str, Path], dst: Union[str, Path]):
    """
    Copy a file from local to a docker container.

    Args:
        container (Container): Docker container to copy to
        src (Path): Source file path
        dst (Path): Destination file path in the container
    """
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.is_file():
        raise FileNotFoundError(f"Source file does not exist: {src_path}")

    # Create an in-memory tar archive containing the source file
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        # arcname is the name of the file inside the archive (no leading directories)
        tar.add(src_path, arcname=dst_path.name)
    tar_stream.seek(0)

    # The destination directory inside the container
    dest_dir = str(dst_path.parent)

    # Put the archive into the container
    # container.put_archive returns a bool indicating success
    success = container.put_archive(dest_dir, tar_stream.read())
    if not success:
        raise RuntimeError(f"Failed to copy {src_path} to {container.id}:{dest_dir}")
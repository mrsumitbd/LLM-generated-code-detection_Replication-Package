def copy_to_container(container: Container, src: Path, dst: Path):
    """
    Copy a file from local to a docker container

    Args:
        container (Container): Docker container to copy to
        src (Path): Source file path
        dst (Path): Destination file path in the container
    """
    container.put_archive(str(dst.parent), tarfile.open(mode='w').add(str(src), os.path.basename(dst)))
from pathlib import Path
from docker.models.containers import Container

def write_to_container(container: Container, data: str, dst: Path):
    """
    Write a string to a file in a docker container
    """
    # echo with heredoc to file
    command = f"cat <<'{HEREDOC_DELIMITER}' > {dst}\n{data}\n{HEREDOC_DELIMITER}"
    container.exec_run(command)
import tempfile
from env.base import Env
from typing import Any, Iterator, cast

def download_db_from_docker(container_id: str, env: Env) -> Iterator[str]:
    # Get the database file self.sqlite_database from the running container using docker API.
    db_stream = load_file_from_docker(
        container_id, env.workdir + "/" + env.sqlite_database
    )
    with tempfile.TemporaryDirectory() as tempdir:
        filename = tempdir + "/" + env.sqlite_database
        with open(filename, "wb") as f:
            f.write(db_stream)
        yield filename
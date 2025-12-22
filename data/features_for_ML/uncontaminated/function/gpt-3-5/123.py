from typing import List, Dict, Union

def run(
        image: str,
        command: List[str],
        volumes: Dict[str, str] | None = None,
        device_requests: List[Union[int, str]] | None = None,
        environment: Dict[str, str] | None = None,
        network: str | None = None,
        detach: bool = False,
        remove: bool = False,
        ports: Dict[int, int] | None = None,
        stdout: bool = True,
        stderr: bool = False,
        user: str | None = None,
        extra_args: List[str] | None = None,
    ) -> Container | tuple[bytes, bytes] | bytes:
        pass
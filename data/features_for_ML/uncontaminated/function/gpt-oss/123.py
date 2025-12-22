import subprocess
from typing import Any, Dict, List, Tuple, Union

def run(
        image: str,
        command: List[str],  # noqa: UP006
        volumes: Dict[str, str] | None = None,
        device_requests: List[int | str] | None = None,  # noqa: UP006
        environment: Dict[str, str] | None = None,
        network: str | None = None,
        detach: bool = False,
        remove: bool = False,
        ports: Dict[str, str] | None = None,
        stdout: bool = True,
        stderr: bool = False,
        user: str | None = None,
        extra_args: List[str] | None = None,  # noqa: UP006
    ) -> Union[str, Tuple[bytes, bytes], bytes]:
    """
    Run a command in a container from an image.

    Parameters
    ----------
    image : str
        The image name or id to run the command in.
    command : list[str]
        The command to run in the container.
    volumes : dict | None
        A dict of volumes to mount in the container.
    device_requests : list[int | str] | None
        A list of device requests for the container.
    environment : dict[str, str] | None
        Environment variables to set in the container.
    network : str | None
        Network to connect the container to.
    detach : bool
        If True, run the container in detached mode.
    remove : bool
        If True, the container will automatically remove itself after it finishes executing.
    ports : dict | None
        A dict of ports to expose in the container. The keys are the host ports
        and the values are the container ports.
    stdout : bool
        If True, return stdout.
    stderr : bool
        If True, return stderr.
    user : str | None
        String of user information to run command as in the format "uid:(optional)gid".
    extra_args : list[str] | None
        Additional arguments to pass to the `docker run` CLI command.

    Returns
    -------
    Container object if detach is True, otherwise returns list of stdout and stderr.
    """
    if detach and remove:
        raise ValueError("Cannot set both detach and remove to True")

    cmd: List[str] = ["docker", "run"]

    if detach:
        cmd.append("--detach")
    if remove:
        cmd.append("--rm")
    if network:
        cmd.extend(["--network", network])
    if user:
        cmd.extend(["--user", user])
    if environment:
        for k, v in environment.items():
            cmd.extend(["-e", f"{k}={v}"])
    if volumes:
        for host_path, container_path in volumes.items():
            cmd.extend(["-v", f"{host_path}:{container_path}"])
    if ports:
        for host_port, container_port in ports.items():
            cmd.extend(["-p", f"{host_port}:{container_port}"])
    if device_requests:
        for dev in device_requests:
            cmd.extend(["--device", str(dev)])
    if extra_args:
        cmd.extend(extra_args)

    cmd.append(image)
    cmd.extend(command)

    try:
        if detach:
            result = subprocess.run(
                cmd,
                capture_output=True,
                check=True,
                text=False,
            )
            # Return container ID as a string
            return result.stdout.decode().strip()
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                check=True,
                text=False,
            )
            out = result.stdout
            err = result.stderr
            if stdout and stderr:
                return (out, err)
            if stdout:
                return out
            if stderr:
                return err
            return b""
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"docker run failed: {exc.stderr.decode() if exc.stderr else exc}"
        ) from exc
import shlex
import subprocess
from typing import List as list_
from tesseract_core.sdk.config import get_config

def run(
        image: str,
        command: list_[str],  # noqa: UP006
        volumes: dict | None = None,
        device_requests: list_[int | str] | None = None,  # noqa: UP006
        environment: dict[str, str] | None = None,
        network: str | None = None,
        detach: bool = False,
        remove: bool = False,
        ports: dict | None = None,
        stdout: bool = True,
        stderr: bool = False,
        user: str | None = None,
        extra_args: list_[str] | None = None,  # noqa: UP006
    ) -> Container | tuple[bytes, bytes] | bytes:
        """Run a command in a container from an image.

        Params:
            image: The image name or id to run the command in.
            command: The command to run in the container.
            volumes: A dict of volumes to mount in the container.
            user: String of user information to run command as in the format "uid:(optional)gid".
            device_requests: A list of device requests for the container.
            detach: If True, run the container in detached mode. Detach must be set to
                    True if we wish to retrieve the container id of the running container,
                    and if detach is true, we must wait on the container to finish
                    running and retrieve the logs of the container manually.
            remove: If remove is set to True, the container will automatically remove itself
                    after it finishes executing the command. This means that we cannot set
                    both detach and remove simulataneously to True or else there
                    would be no way of retrieving the logs from the removed container.
            ports: A dict of ports to expose in the container. The keys are the host ports
                   and the values are the container ports.
            stdout: If True, return stdout.
            stderr: If True, return stderr.
            environment: Environment variables to set in the container.
            extra_args: Additional arguments to pass to the `docker run` CLI command.

        Returns:
            Container object if detach is True, otherwise returns list of stdout and stderr.
        """
        config = get_config()
        docker = _get_docker_executable()

        if isinstance(command, str):
            command = [command]

        optional_args = []

        # Convert the parsed_volumes into a list of strings in proper argument format,
        # `-v host_path:container_path:mode`.
        if volumes:
            volume_args = []
            for host_path, volume_info in volumes.items():
                volume_args.append("-v")
                volume_args.append(
                    f"{host_path}:{volume_info['bind']}:{volume_info['mode']}"
                )
            optional_args.extend(volume_args)

        if network:
            optional_args.extend(["--network", network])

        if user:
            optional_args.extend(["-u", user])

        if device_requests:
            gpus_str = ",".join(device_requests)
            optional_args.extend(["--gpus", f'"device={gpus_str}"'])

        if environment:
            env_args = []
            for env_var, value in environment.items():
                env_args.extend(["-e", f"{env_var}={value}"])
            optional_args.extend(env_args)

        # Remove and detached cannot both be set to true
        if remove and detach:
            raise ValueError(
                "Cannot set both remove and detach to True when running a container."
            )
        if detach:
            optional_args.append("--detach")
        if remove:
            optional_args.append("--rm")

        if ports:
            for host_port, container_port in ports.items():
                optional_args.extend(["-p", f"{host_port}:{container_port}"])

        if extra_args is None:
            extra_args = []

        full_cmd = [
            *docker,
            "run",
            *optional_args,
            *config.docker_run_args,
            *extra_args,
            image,
            *command,
        ]

        logger.debug(f"Running command: {full_cmd}")

        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=False,
            check=False,
        )

        if result.returncode != 0:
            stderr_str = result.stderr.decode("utf-8", errors="ignore")
            if "repository" in stderr_str:
                raise ImageNotFound(stderr_str)
            raise ContainerError(
                None,
                result.returncode,
                shlex.join(full_cmd),
                image,
                result.stderr,
            )

        if detach:
            # If detach is True, stdout prints out the container ID of the running container
            container_id = result.stdout.decode("utf-8", errors="ignore").strip()
            container_obj = Containers.get(container_id)
            return container_obj

        if stdout and stderr:
            return result.stdout, result.stderr
        if stderr:
            return result.stderr
        return result.stdout
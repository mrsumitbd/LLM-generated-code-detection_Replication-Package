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
    import docker
    
    client = docker.from_env()
    
    kwargs = {
        'image': image,
        'command': command,
        'detach': detach,
        'remove': remove,
        'stdout': stdout,
        'stderr': stderr,
    }
    
    if volumes is not None:
        kwargs['volumes'] = volumes
    
    if device_requests is not None:
        kwargs['device_requests'] = [
            docker.types.DeviceRequest(device_ids=[str(d)]) if isinstance(d, int) else docker.types.DeviceRequest(device_ids=[d])
            for d in device_requests
        ]
    
    if environment is not None:
        kwargs['environment'] = environment
    
    if network is not None:
        kwargs['network'] = network
    
    if ports is not None:
        kwargs['ports'] = ports
    
    if user is not None:
        kwargs['user'] = user
    
    if extra_args is not None:
        kwargs['extra_args'] = extra_args
    
    container = client.containers.run(**kwargs)
    
    if detach:
        return container
    else:
        if stdout and stderr:
            return (container, container)
        elif stdout:
            return container
        elif stderr:
            return container
        else:
            return container
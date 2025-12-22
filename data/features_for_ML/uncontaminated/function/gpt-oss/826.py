import logging

def _cleanup_orphan_bridges():
    """
    Remove Docker bridge networks that have no containers attached.
    """
    logger = logging.getLogger(__name__)
    try:
        import docker
    except Exception:
        # Docker SDK not available; nothing to clean up
        return

    try:
        client = docker.from_env()
    except Exception as exc:
        logger.debug("Failed to create Docker client: %s", exc)
        return

    try:
        networks = client.networks.list()
    except Exception as exc:
        logger.debug("Failed to list Docker networks: %s", exc)
        return

    for net in networks:
        try:
            attrs = net.attrs
        except Exception:
            continue

        driver = attrs.get("Driver")
        if driver != "bridge":
            continue

        containers = attrs.get("Containers", {})
        if not containers:
            try:
                net.remove()
                logger.info("Removed orphan bridge network %s", net.name)
            except Exception as exc:
                logger.debug("Failed to remove network %s: %s", net.name, exc)
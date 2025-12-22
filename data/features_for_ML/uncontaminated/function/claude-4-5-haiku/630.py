def download_db_from_docker(container_id: str, env: Env) -> Iterator[str]:
    import docker
    import io
    
    client = docker.from_env()
    container = client.containers.get(container_id)
    
    db_path = env.sqlite_database
    
    try:
        bits, stat = container.get_archive(db_path)
        for chunk in bits:
            yield chunk.decode('utf-8', errors='ignore')
    except docker.errors.NotFound:
        raise FileNotFoundError(f"Database file {db_path} not found in container {container_id}")
    except docker.errors.APIError as e:
        raise RuntimeError(f"Docker API error: {str(e)}")
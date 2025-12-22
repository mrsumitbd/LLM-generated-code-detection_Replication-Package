from typing import Optional

class DockerImageBuilder:
    """
    Builder for creating custom Docker images with user specifications.
    
    Provides a fluent API for configuring Docker images with system packages,
    Python packages, custom commands, and environment variables.
    """

    def __init__(self, base_image: str = "python:3.11-slim"):
        self.base_image = base_image
        self.instructions = []

    def add_system_packages(self, *packages: str) -> 'DockerImageBuilder':
        self.instructions.extend([f"RUN apt-get update && apt-get install -y {pkg}" for pkg in packages])
        return self

    def add_python_packages(self, *packages: str) -> 'DockerImageBuilder':
        self.instructions.extend([f"RUN pip install {pkg}" for pkg in packages])
        return self

    def add_custom_command(self, command: str) -> 'DockerImageBuilder':
        self.instructions.append(f"RUN {command}")
        return self

    def set_environment(self, **env_vars: str) -> 'DockerImageBuilder':
        self.instructions.extend([f"ENV {key}={value}" for key, value in env_vars.items()])
        return self

    def set_working_directory(self, path: str) -> 'DockerImageBuilder':
        self.instructions.append(f"WORKDIR {path}")
        return self

    def set_user(self, user_id: int = 1000, user_name: str = "tinyagent") -> 'DockerImageBuilder':
        self.instructions.append(f"USER {user_id}:{user_name}")
        return self

    def copy_file(self, source_path: str, container_path: str) -> 'DockerImageBuilder':
        self.instructions.append(f"COPY {source_path} {container_path}")
        return self

    def expose_port(self, port: int) -> 'DockerImageBuilder':
        self.instructions.append(f"EXPOSE {port}")
        return self

    def add_volume(self, path: str) -> 'DockerImageBuilder':
        self.instructions.append(f"VOLUME {path}")
        return self

    def generate_dockerfile(self) -> str:
        return '\n'.join(self.instructions)

    def get_image_tag(self) -> str:
        return self.base_image

    def save_dockerfile(self, path: Optional[str] = None) -> str:
        dockerfile_content = self.generate_dockerfile()
        if path:
            with open(path, 'w') as f:
                f.write(dockerfile_content)
        return dockerfile_content
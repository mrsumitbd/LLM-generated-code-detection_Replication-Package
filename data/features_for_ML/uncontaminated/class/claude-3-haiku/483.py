from typing import Optional

class DockerImageBuilder:
    """
    Builder for creating custom Docker images with user specifications.
    
    Provides a fluent API for configuring Docker images with system packages,
    Python packages, custom commands, and environment variables.
    """

    def __init__(self, base_image: str = "python:3.11-slim"):
        self.base_image = base_image
        self.system_packages = []
        self.python_packages = []
        self.custom_commands = []
        self.environment_variables = {}
        self.working_directory = None
        self.user_id = 1000
        self.user_name = "tinyagent"
        self.copied_files = []
        self.exposed_ports = []
        self.volumes = []

    def add_system_packages(self, *packages: str) -> 'DockerImageBuilder':
        self.system_packages.extend(packages)
        return self

    def add_python_packages(self, *packages: str) -> 'DockerImageBuilder':
        self.python_packages.extend(packages)
        return self

    def add_custom_command(self, command: str) -> 'DockerImageBuilder':
        self.custom_commands.append(command)
        return self

    def set_environment(self, **env_vars: str) -> 'DockerImageBuilder':
        self.environment_variables.update(env_vars)
        return self

    def set_working_directory(self, path: str) -> 'DockerImageBuilder':
        self.working_directory = path
        return self

    def set_user(self, user_id: int = 1000, user_name: str = "tinyagent") -> 'DockerImageBuilder':
        self.user_id = user_id
        self.user_name = user_name
        return self

    def copy_file(self, source_path: str, container_path: str) -> 'DockerImageBuilder':
        self.copied_files.append((source_path, container_path))
        return self

    def expose_port(self, port: int) -> 'DockerImageBuilder':
        self.exposed_ports.append(port)
        return self

    def add_volume(self, path: str) -> 'DockerImageBuilder':
        self.volumes.append(path)
        return self

    def generate_dockerfile(self) -> str:
        dockerfile = f"FROM {self.base_image}\n"

        if self.system_packages:
            dockerfile += f"RUN apt-get update && apt-get install -y {' '.join(self.system_packages)}\n"

        if self.python_packages:
            dockerfile += f"RUN pip install {' '.join(self.python_packages)}\n"

        if self.custom_commands:
            for command in self.custom_commands:
                dockerfile += f"RUN {command}\n"

        if self.environment_variables:
            for key, value in self.environment_variables.items():
                dockerfile += f"ENV {key}={value}\n"

        if self.working_directory:
            dockerfile += f"WORKDIR {self.working_directory}\n"

        dockerfile += f"RUN useradd -u {self.user_id} -m {self.user_name}\n"
        dockerfile += f"USER {self.user_name}\n"

        for source_path, container_path in self.copied_files:
            dockerfile += f"COPY {source_path} {container_path}\n"

        for port in self.exposed_ports:
            dockerfile += f"EXPOSE {port}\n"

        for volume in self.volumes:
            dockerfile += f"VOLUME {volume}\n"

        return dockerfile

    def get_image_tag(self) -> str:
        return f"{self.base_image.replace(':', '-')}-custom"

    def save_dockerfile(self, path: Optional[str] = None) -> str:
        dockerfile = self.generate_dockerfile()
        if path:
            with open(path, "w") as file:
                file.write(dockerfile)
        return dockerfile
from typing import Optional
from datetime import datetime
import os


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
        self.environment_vars = {}
        self.working_directory = None
        self.user_id = None
        self.user_name = None
        self.files_to_copy = []
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
        self.environment_vars.update(env_vars)
        return self

    def set_working_directory(self, path: str) -> 'DockerImageBuilder':
        self.working_directory = path
        return self

    def set_user(self, user_id: int = 1000, user_name: str = "tinyagent") -> 'DockerImageBuilder':
        self.user_id = user_id
        self.user_name = user_name
        return self

    def copy_file(self, source_path: str, container_path: str) -> 'DockerImageBuilder':
        self.files_to_copy.append((source_path, container_path))
        return self

    def expose_port(self, port: int) -> 'DockerImageBuilder':
        self.exposed_ports.append(port)
        return self

    def add_volume(self, path: str) -> 'DockerImageBuilder':
        self.volumes.append(path)
        return self

    def generate_dockerfile(self) -> str:
        lines = []
        
        # Base image
        lines.append(f"FROM {self.base_image}")
        lines.append("")
        
        # System packages
        if self.system_packages:
            lines.append("RUN apt-get update && apt-get install -y \\")
            for i, package in enumerate(self.system_packages):
                if i < len(self.system_packages) - 1:
                    lines.append(f"    {package} \\")
                else:
                    lines.append(f"    {package}")
            lines.append("&& rm -rf /var/lib/apt/lists/*")
            lines.append("")
        
        # Python packages
        if self.python_packages:
            lines.append("RUN pip install --no-cache-dir \\")
            for i, package in enumerate(self.python_packages):
                if i < len(self.python_packages) - 1:
                    lines.append(f"    {package} \\")
                else:
                    lines.append(f"    {package}")
            lines.append("")
        
        # Environment variables
        for key, value in self.environment_vars.items():
            lines.append(f"ENV {key}={value}")
        if self.environment_vars:
            lines.append("")
        
        # Working directory
        if self.working_directory:
            lines.append(f"WORKDIR {self.working_directory}")
            lines.append("")
        
        # Copy files
        for source, container in self.files_to_copy:
            lines.append(f"COPY {source} {container}")
        if self.files_to_copy:
            lines.append("")
        
        # Custom commands
        for command in self.custom_commands:
            lines.append(f"RUN {command}")
        if self.custom_commands:
            lines.append("")
        
        # Expose ports
        for port in self.exposed_ports:
            lines.append(f"EXPOSE {port}")
        if self.exposed_ports:
            lines.append("")
        
        # Volumes
        for volume in self.volumes:
            lines.append(f"VOLUME {volume}")
        if self.volumes:
            lines.append("")
        
        # User
        if self.user_id is not None and self.user_name:
            lines.append(f"RUN useradd -m -u {self.user_id} {self.user_name}")
            lines.append(f"USER {self.user_name}")
            lines.append("")
        
        # Remove trailing empty lines
        while lines and lines[-1] == "":
            lines.pop()
        
        return "\n".join(lines)

    def get_image_tag(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"custom-image:{timestamp}"

    def save_dockerfile(self, path: Optional[str] = None) -> str:
        if path is None:
            path = "Dockerfile"
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        dockerfile_content = self.generate_dockerfile()
        
        with open(path, 'w') as f:
            f.write(dockerfile_content)
        
        return path
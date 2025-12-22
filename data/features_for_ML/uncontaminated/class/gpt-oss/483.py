from __future__ import annotations
import hashlib
import os
import time
from typing import List, Tuple, Optional, Dict


class DockerImageBuilder:
    """
    Builder for creating custom Docker images with user specifications.
    
    Provides a fluent API for configuring Docker images with system packages,
    Python packages, custom commands, and environment variables.
    """

    def __init__(self, base_image: str = "python:3.11-slim"):
        self.base_image: str = base_image
        self.system_packages: List[str] = []
        self.python_packages: List[str] = []
        self.custom_commands: List[str] = []
        self.env_vars: Dict[str, str] = {}
        self.working_directory: Optional[str] = None
        self.user_id: Optional[int] = None
        self.user_name: Optional[str] = None
        self.copy_files: List[Tuple[str, str]] = []
        self.exposed_ports: List[int] = []
        self.volumes: List[str] = []

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
        self.env_vars.update(env_vars)
        return self

    def set_working_directory(self, path: str) -> 'DockerImageBuilder':
        self.working_directory = path
        return self

    def set_user(self, user_id: int = 1000, user_name: str = "tinyagent") -> 'DockerImageBuilder':
        self.user_id = user_id
        self.user_name = user_name
        return self

    def copy_file(self, source_path: str, container_path: str) -> 'DockerImageBuilder':
        self.copy_files.append((source_path, container_path))
        return self

    def expose_port(self, port: int) -> 'DockerImageBuilder':
        self.exposed_ports.append(port)
        return self

    def add_volume(self, path: str) -> 'DockerImageBuilder':
        self.volumes.append(path)
        return self

    def generate_dockerfile(self) -> str:
        lines: List[str] = [f"FROM {self.base_image}"]

        if self.system_packages:
            pkgs = " ".join(self.system_packages)
            lines.append(f"RUN apt-get update && apt-get install -y {pkgs} && rm -rf /var/lib/apt/lists/*")

        if self.python_packages:
            pkgs = " ".join(self.python_packages)
            lines.append(f"RUN pip install --no-cache-dir {pkgs}")

        if self.copy_files:
            for src, dst in self.copy_files:
                lines.append(f"COPY {src} {dst}")

        if self.working_directory:
            lines.append(f"WORKDIR {self.working_directory}")

        if self.env_vars:
            for key, value in self.env_vars.items():
                lines.append(f"ENV {key}={value}")

        if self.user_id is not None and self.user_name is not None:
            lines.append(f"RUN useradd -m -u {self.user_id} {self.user_name}")
            lines.append(f"USER {self.user_name}")

        if self.exposed_ports:
            ports = " ".join(str(p) for p in self.exposed_ports)
            lines.append(f"EXPOSE {ports}")

        if self.volumes:
            for vol in self.volumes:
                lines.append(f"VOLUME {vol}")

        lines.extend(self.custom_commands)

        return "\n".join(lines) + "\n"

    def get_image_tag(self) -> str:
        # Create a deterministic tag based on base image and package lists
        tag_source = (
            self.base_image
            + "|"
            + ",".join(sorted(self.system_packages))
            + "|"
            + ",".join(sorted(self.python_packages))
            + "|"
            + ",".join(sorted(self.env_vars.items()))
            + "|"
            + ",".join(self.custom_commands)
        )
        hash_digest = hashlib.sha256(tag_source.encode()).hexdigest()[:8]
        timestamp = int(time.time())
        base_tag = self.base_image.replace(":", "-").replace("/", "_")
        return f"{base_tag}-{hash_digest}-{timestamp}"

    def save_dockerfile(self, path: Optional[str] = None) -> str:
        if path is None:
            path = "Dockerfile"
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.generate_dockerfile())
        return os.path.abspath(path)
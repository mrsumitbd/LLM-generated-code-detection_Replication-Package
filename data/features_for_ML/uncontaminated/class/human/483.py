import os
from typing import Dict, List, Optional, Union, Any
import tempfile
import hashlib

class DockerImageBuilder:
    """
    Builder for creating custom Docker images with user specifications.
    
    Provides a fluent API for configuring Docker images with system packages,
    Python packages, custom commands, and environment variables.
    """
    
    def __init__(self, base_image: str = "python:3.11-slim"):
        """
        Initialize the Docker image builder.
        
        Args:
            base_image: Base Docker image to build from
        """
        self.base_image = base_image
        self.system_packages = []
        self.pip_packages = []
        self.custom_commands = []
        self.environment_vars = {}
        self.working_directory = "/workspace"
        self.user_id = 1000
        self.user_name = "tinyagent"
        self.copy_files = {}  # source_path -> container_path
        self.expose_ports = []
        self.volumes = []
        
    def add_system_packages(self, *packages: str) -> 'DockerImageBuilder':
        """
        Add system packages to be installed via apt-get.
        
        Args:
            *packages: Package names to install
            
        Returns:
            Self for method chaining
        """
        self.system_packages.extend(packages)
        return self
    
    def add_python_packages(self, *packages: str) -> 'DockerImageBuilder':
        """
        Add Python packages to be installed via pip.
        
        Args:
            *packages: Package names to install
            
        Returns:
            Self for method chaining
        """
        self.pip_packages.extend(packages)
        return self
    
    def add_custom_command(self, command: str) -> 'DockerImageBuilder':
        """
        Add a custom RUN command to the Dockerfile.
        
        Args:
            command: Shell command to execute during build
            
        Returns:
            Self for method chaining
        """
        self.custom_commands.append(command)
        return self
    
    def set_environment(self, **env_vars: str) -> 'DockerImageBuilder':
        """
        Set environment variables in the container.
        
        Args:
            **env_vars: Environment variables as key-value pairs
            
        Returns:
            Self for method chaining
        """
        self.environment_vars.update(env_vars)
        return self
    
    def set_working_directory(self, path: str) -> 'DockerImageBuilder':
        """
        Set the working directory in the container.
        
        Args:
            path: Working directory path
            
        Returns:
            Self for method chaining
        """
        self.working_directory = path
        return self
    
    def set_user(self, user_id: int = 1000, user_name: str = "tinyagent") -> 'DockerImageBuilder':
        """
        Set the user for container execution.
        
        Args:
            user_id: User ID number
            user_name: Username
            
        Returns:
            Self for method chaining
        """
        self.user_id = user_id
        self.user_name = user_name
        return self
    
    def copy_file(self, source_path: str, container_path: str) -> 'DockerImageBuilder':
        """
        Copy a file or directory into the container during build.
        
        Args:
            source_path: Path on host system
            container_path: Destination path in container
            
        Returns:
            Self for method chaining
        """
        self.copy_files[source_path] = container_path
        return self
    
    def expose_port(self, port: int) -> 'DockerImageBuilder':
        """
        Expose a port in the container.
        
        Args:
            port: Port number to expose
            
        Returns:
            Self for method chaining
        """
        self.expose_ports.append(port)
        return self
    
    def add_volume(self, path: str) -> 'DockerImageBuilder':
        """
        Add a volume mount point.
        
        Args:
            path: Path to create as volume mount point
            
        Returns:
            Self for method chaining
        """
        self.volumes.append(path)
        return self
    
    def generate_dockerfile(self) -> str:
        """
        Generate Dockerfile content based on configuration.
        
        Returns:
            Dockerfile content as string
        """
        lines = []
        
        # Base image
        lines.append(f"FROM {self.base_image}")
        lines.append("")
        
        # System packages installation
        if self.system_packages:
            lines.append("# Install system packages")
            packages_str = " \\\n    ".join(self.system_packages)
            lines.append(f"RUN apt-get update && apt-get install -y \\")
            lines.append(f"    {packages_str} \\")
            lines.append("    && rm -rf /var/lib/apt/lists/*")
            lines.append("")
        
        # Python packages installation
        if self.pip_packages:
            lines.append("# Install Python packages")
            packages_str = " \\\n    ".join(self.pip_packages)
            lines.append(f"RUN pip install --no-cache-dir \\")
            lines.append(f"    {packages_str}")
            lines.append("")
        
        # Environment variables
        if self.environment_vars:
            lines.append("# Set environment variables")
            for key, value in self.environment_vars.items():
                lines.append(f"ENV {key}={value}")
            lines.append("")
        
        # Copy files
        if self.copy_files:
            lines.append("# Copy files")
            for source, dest in self.copy_files.items():
                lines.append(f"COPY {source} {dest}")
            lines.append("")
        
        # Custom commands
        if self.custom_commands:
            lines.append("# Custom commands")
            for command in self.custom_commands:
                lines.append(f"RUN {command}")
            lines.append("")
        
        # Create user and set permissions
        lines.append("# Create non-root user")
        lines.append(f"RUN useradd -m -u {self.user_id} {self.user_name}")
        
        # Create working directory and set permissions
        lines.append(f"RUN mkdir -p {self.working_directory}")
        lines.append(f"RUN chown -R {self.user_name}:{self.user_name} {self.working_directory}")
        
        # Create volume mount points
        for volume in self.volumes:
            lines.append(f"RUN mkdir -p {volume}")
            lines.append(f"RUN chown -R {self.user_name}:{self.user_name} {volume}")
        
        lines.append("")
        
        # Expose ports
        if self.expose_ports:
            lines.append("# Expose ports")
            for port in self.expose_ports:
                lines.append(f"EXPOSE {port}")
            lines.append("")
        
        # Volume declarations
        if self.volumes:
            lines.append("# Volume mount points")
            for volume in self.volumes:
                lines.append(f"VOLUME {volume}")
            lines.append("")
        
        # Switch to non-root user
        lines.append(f"USER {self.user_name}")
        lines.append(f"WORKDIR {self.working_directory}")
        lines.append("")
        
        # Health check
        lines.append("# Health check")
        lines.append("HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\")
        lines.append('    CMD python3 -c "print(\'Container healthy\')" || exit 1')
        lines.append("")
        
        # Default command
        lines.append('CMD ["python3"]')
        
        return "\n".join(lines)
    
    def get_image_tag(self) -> str:
        """
        Generate a unique image tag based on configuration.
        
        Returns:
            Docker image tag
        """
        # Create a hash of the configuration for uniqueness
        config_str = (
            f"{self.base_image}|"
            f"{'|'.join(sorted(self.system_packages))}|"
            f"{'|'.join(sorted(self.pip_packages))}|"
            f"{'|'.join(self.custom_commands)}|"
            f"{'|'.join(f'{k}={v}' for k, v in sorted(self.environment_vars.items()))}|"
            f"{self.working_directory}|{self.user_id}|{self.user_name}"
        )
        
        config_hash = hashlib.md5(config_str.encode()).hexdigest()[:12]
        
        # Create a readable tag
        base_name = self.base_image.split(':')[0].replace('/', '-')
        return f"tinyagent-{base_name}-{config_hash}"
    
    def save_dockerfile(self, path: Optional[str] = None) -> str:
        """
        Save the generated Dockerfile to a file.
        
        Args:
            path: Optional path to save the Dockerfile. If None, creates a temporary file.
            
        Returns:
            Path to the saved Dockerfile
        """
        dockerfile_content = self.generate_dockerfile()
        
        if path is None:
            # Create temporary file
            fd, path = tempfile.mkstemp(suffix='.Dockerfile', prefix='tinyagent_')
            with os.fdopen(fd, 'w') as f:
                f.write(dockerfile_content)
        else:
            # Save to specified path
            with open(path, 'w') as f:
                f.write(dockerfile_content)
        
        return path
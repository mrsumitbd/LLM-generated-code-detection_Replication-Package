from typing import Any, Dict

class PodSpec:
    """
    Universal pod specification for Kubernetes-based execution.
    """

    def __init__(self, container_image: str, container_name: str, command: list[str], env: dict[str, str] = None, resources: dict[str, dict[str, str]] = None):
        self.container_image = container_image
        self.container_name = container_name
        self.command = command
        self.env = env or {}
        self.resources = resources or {}

    def to_kubernetes_pod_spec(self) -> dict[str, Any]:
        pod_spec = {
            "containers": [
                {
                    "name": self.container_name,
                    "image": self.container_image,
                    "command": self.command,
                    "env": [{"name": k, "value": v} for k, v in self.env.items()],
                    "resources": self.resources,
                }
            ]
        }
        return pod_spec

    def to_kubernetes_job(self, job_name: str, namespace: str = "default") -> dict[str, Any]:
        job = {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {
                "name": job_name,
                "namespace": namespace,
            },
            "spec": {
                "template": {
                    "spec": self.to_kubernetes_pod_spec()
                }
            }
        }
        return job
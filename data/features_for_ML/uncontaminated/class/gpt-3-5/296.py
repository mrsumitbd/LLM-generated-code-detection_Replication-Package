from typing import Any

class PodSpec:
    """
    Universal pod specification for Kubernetes-based execution.
    """

    def to_kubernetes_pod_spec(self) -> dict[str, Any]:
        return {}

    def to_kubernetes_job(self, job_name: str, namespace: str = "default") -> dict[str, Any]:
        return {}
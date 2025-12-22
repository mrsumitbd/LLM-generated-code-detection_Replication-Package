from dataclasses import dataclass, field
from typing import Any, Optional

class PodSpec:
    """
    Universal pod specification for Kubernetes-based execution.
    """

    # Containers in the pod
    containers: list[ContainerSpec] = field(default_factory=list)

    # Volumes available to containers
    volumes: list[Volume] = field(default_factory=list)

    # Pod-level settings
    restart_policy: str = "Never"
    service_account_name: Optional[str] = None
    node_selector: dict[str, str] = field(default_factory=dict)
    tolerations: list[dict[str, Any]] = field(default_factory=list)
    affinity: Optional[dict[str, Any]] = None

    # Security context
    security_context: dict[str, Any] = field(default_factory=dict)

    # DNS and networking
    dns_policy: str = "ClusterFirst"
    hostname: Optional[str] = None
    subdomain: Optional[str] = None

    # Labels and annotations
    labels: dict[str, str] = field(default_factory=dict)
    annotations: dict[str, str] = field(default_factory=dict)

    def to_kubernetes_pod_spec(self) -> dict[str, Any]:
        """Convert to Kubernetes Pod specification."""
        pod_spec: dict[str, Any] = {
            "restartPolicy": self.restart_policy,
            "containers": [container.to_kubernetes_container() for container in self.containers],
            "volumes": [{"name": volume.name, volume.volume_type: volume.source} for volume in self.volumes],
        }

        if self.service_account_name:
            pod_spec["serviceAccountName"] = self.service_account_name
        if self.node_selector:
            pod_spec["nodeSelector"] = self.node_selector
        if self.tolerations:
            pod_spec["tolerations"] = self.tolerations
        if self.affinity:
            pod_spec["affinity"] = self.affinity
        if self.security_context:
            pod_spec["securityContext"] = self.security_context
        if self.dns_policy:
            pod_spec["dnsPolicy"] = self.dns_policy
        if self.hostname:
            pod_spec["hostname"] = self.hostname
        if self.subdomain:
            pod_spec["subdomain"] = self.subdomain

        return pod_spec

    def to_kubernetes_job(self, job_name: str, namespace: str = "default") -> dict[str, Any]:
        """Convert to Kubernetes Job specification."""
        return {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {
                "name": job_name,
                "namespace": namespace,
                "labels": self.labels,
                "annotations": self.annotations,
            },
            "spec": {
                "ttlSecondsAfterFinished": 3600,
                "backoffLimit": 3,
                "template": {"metadata": {"labels": self.labels}, "spec": self.to_kubernetes_pod_spec()},
            },
        }
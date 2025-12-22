from __future__ import annotations

from typing import Any, Dict, List, Optional


class PodSpec:
    """
    Universal pod specification for Kubernetes-based execution.
    """

    def __init__(
        self,
        containers: List[Dict[str, Any]],
        *,
        volumes: Optional[List[Dict[str, Any]]] = None,
        node_selector: Optional[Dict[str, str]] = None,
        tolerations: Optional[List[Dict[str, Any]]] = None,
        restart_policy: str = "Never",
        image_pull_secrets: Optional[List[Dict[str, str]]] = None,
        labels: Optional[Dict[str, str]] = None,
        annotations: Optional[Dict[str, str]] = None,
    ) -> None:
        self.containers = containers
        self.volumes = volumes or []
        self.node_selector = node_selector or {}
        self.tolerations = tolerations or []
        self.restart_policy = restart_policy
        self.image_pull_secrets = image_pull_secrets or []
        self.labels = labels or {}
        self.annotations = annotations or {}

    def to_kubernetes_pod_spec(self) -> Dict[str, Any]:
        pod_spec: Dict[str, Any] = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "labels": self.labels,
                "annotations": self.annotations,
            },
            "spec": {
                "containers": self.containers,
                "restartPolicy": self.restart_policy,
            },
        }

        if self.volumes:
            pod_spec["spec"]["volumes"] = self.volumes
        if self.node_selector:
            pod_spec["spec"]["nodeSelector"] = self.node_selector
        if self.tolerations:
            pod_spec["spec"]["tolerations"] = self.tolerations
        if self.image_pull_secrets:
            pod_spec["spec"]["imagePullSecrets"] = self.image_pull_secrets

        return pod_spec

    def to_kubernetes_job(
        self,
        job_name: str,
        namespace: str = "default",
    ) -> Dict[str, Any]:
        job_spec: Dict[str, Any] = {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {
                "name": job_name,
                "namespace": namespace,
                "labels": self.labels,
                "annotations": self.annotations,
            },
            "spec": {
                "template": {
                    "metadata": {
                        "labels": self.labels,
                        "annotations": self.annotations,
                    },
                    "spec": {
                        "containers": self.containers,
                        "restartPolicy": self.restart_policy,
                        "backoffLimit": 4,
                    },
                },
            },
        }

        if self.volumes:
            job_spec["spec"]["template"]["spec"]["volumes"] = self.volumes
        if self.node_selector:
            job_spec["spec"]["template"]["spec"]["nodeSelector"] = self.node_selector
        if self.tolerations:
            job_spec["spec"]["template"]["spec"]["tolerations"] = self.tolerations
        if self.image_pull_secrets:
            job_spec["spec"]["template"]["spec"]["imagePullSecrets"] = self.image_pull_secrets

        return job_spec
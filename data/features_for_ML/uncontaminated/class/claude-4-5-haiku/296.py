class PodSpec:
    """
    Universal pod specification for Kubernetes-based execution.
    """

    def __init__(
        self,
        image: str,
        command: list[str] | None = None,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
        resources: dict[str, Any] | None = None,
        volume_mounts: list[dict[str, Any]] | None = None,
        volumes: list[dict[str, Any]] | None = None,
        image_pull_policy: str = "IfNotPresent",
        restart_policy: str = "Never",
        service_account_name: str | None = None,
        labels: dict[str, str] | None = None,
        annotations: dict[str, str] | None = None,
    ):
        self.image = image
        self.command = command
        self.args = args
        self.env = env or {}
        self.resources = resources
        self.volume_mounts = volume_mounts or []
        self.volumes = volumes or []
        self.image_pull_policy = image_pull_policy
        self.restart_policy = restart_policy
        self.service_account_name = service_account_name
        self.labels = labels or {}
        self.annotations = annotations or {}

    def to_kubernetes_pod_spec(self) -> dict[str, Any]:
        """Convert to Kubernetes PodSpec format."""
        container_spec: dict[str, Any] = {
            "name": "main",
            "image": self.image,
            "imagePullPolicy": self.image_pull_policy,
        }

        if self.command:
            container_spec["command"] = self.command

        if self.args:
            container_spec["args"] = self.args

        if self.env:
            container_spec["env"] = [
                {"name": key, "value": str(value)} for key, value in self.env.items()
            ]

        if self.resources:
            container_spec["resources"] = self.resources

        if self.volume_mounts:
            container_spec["volumeMounts"] = self.volume_mounts

        pod_spec: dict[str, Any] = {
            "containers": [container_spec],
            "restartPolicy": self.restart_policy,
        }

        if self.volumes:
            pod_spec["volumes"] = self.volumes

        if self.service_account_name:
            pod_spec["serviceAccountName"] = self.service_account_name

        return pod_spec

    def to_kubernetes_job(self, job_name: str, namespace: str = "default") -> dict[str, Any]:
        """Convert to Kubernetes Job format."""
        job: dict[str, Any] = {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {
                "name": job_name,
                "namespace": namespace,
            },
            "spec": {
                "template": {
                    "metadata": {},
                    "spec": self.to_kubernetes_pod_spec(),
                }
            },
        }

        if self.labels:
            job["metadata"]["labels"] = self.labels
            job["spec"]["template"]["metadata"]["labels"] = self.labels

        if self.annotations:
            job["metadata"]["annotations"] = self.annotations
            job["spec"]["template"]["metadata"]["annotations"] = self.annotations

        return job
class KubernetesClient:

    def __init__(self, kube_config_path=None):
        self.kube_config_path = kube_config_path

    def list_pods(self, namespace: str = "default") -> list | str | None:
        # Implementation for listing pods goes here
        pass

    def get_pod_logs(self, pod_name: str, namespace: str = "default") -> list | str:
        # Implementation for getting pod logs goes here
        pass

    def get_pod_health(self, pod_name: str, namespace: str = "default") -> dict:
        # Implementation for getting pod health goes here
        pass
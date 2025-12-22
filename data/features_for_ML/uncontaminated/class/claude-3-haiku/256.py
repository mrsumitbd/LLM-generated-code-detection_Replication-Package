import os
from kubernetes import client, config

class KubernetesClient:

    def __init__(self, kube_config_path=None):
        if kube_config_path:
            config.load_kube_config(config_file=kube_config_path)
        else:
            config.load_incluster_config()
        self.api_client = client.CoreV1Api()

    def list_pods(self, namespace: str = "default") -> list | str | None:
        try:
            pods = self.api_client.list_namespaced_pod(namespace=namespace)
            return [pod.metadata.name for pod in pods.items]
        except client.exceptions.ApiException as e:
            return str(e)

    def get_pod_logs(self, pod_name: str, namespace: str = "default") -> list | str:
        try:
            logs = self.api_client.read_namespaced_pod_log(name=pod_name, namespace=namespace)
            return logs.splitlines()
        except client.exceptions.ApiException as e:
            return str(e)

    def get_pod_health(self, pod_name: str, namespace: str = "default") -> dict:
        try:
            pod = self.api_client.read_namespaced_pod(name=pod_name, namespace=namespace)
            return {
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "ready": pod.status.conditions[-1].type == "Ready" and pod.status.conditions[-1].status == "True"
            }
        except client.exceptions.ApiException as e:
            return {"error": str(e)}
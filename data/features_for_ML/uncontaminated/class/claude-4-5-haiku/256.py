from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Optional


class KubernetesClient:

    def __init__(self, kube_config_path=None):
        try:
            if kube_config_path:
                config.load_kube_config(config_file=kube_config_path)
            else:
                config.load_kube_config()
        except config.ConfigException:
            config.load_incluster_config()
        
        self.v1 = client.CoreV1Api()

    def list_pods(self, namespace: str = "default") -> list | str | None:
        try:
            pods = self.v1.list_namespaced_pod(namespace=namespace)
            pod_list = []
            for pod in pods.items:
                pod_list.append({
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "ready": self._get_pod_ready_status(pod)
                })
            return pod_list
        except ApiException as e:
            return f"Exception when calling CoreV1Api->list_namespaced_pod: {e}"
        except Exception as e:
            return None

    def get_pod_logs(self, pod_name: str, namespace: str = "default") -> list | str:
        try:
            logs = self.v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace
            )
            return logs.split('\n') if logs else []
        except ApiException as e:
            return f"Exception when calling CoreV1Api->read_namespaced_pod_log: {e}"

    def get_pod_health(self, pod_name: str, namespace: str = "default") -> dict:
        try:
            pod = self.v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            
            health_status = {
                "pod_name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "phase": pod.status.phase,
                "ready": self._get_pod_ready_status(pod),
                "containers": []
            }
            
            if pod.status.container_statuses:
                for container in pod.status.container_statuses:
                    container_info = {
                        "name": container.name,
                        "ready": container.ready,
                        "restart_count": container.restart_count,
                        "state": self._get_container_state(container)
                    }
                    health_status["containers"].append(container_info)
            
            if pod.status.conditions:
                health_status["conditions"] = []
                for condition in pod.status.conditions:
                    health_status["conditions"].append({
                        "type": condition.type,
                        "status": condition.status,
                        "reason": condition.reason,
                        "message": condition.message
                    })
            
            return health_status
        except ApiException as e:
            return {"error": f"Exception when calling CoreV1Api->read_namespaced_pod: {e}"}

    def _get_pod_ready_status(self, pod) -> bool:
        if pod.status.conditions:
            for condition in pod.status.conditions:
                if condition.type == "Ready":
                    return condition.status == "True"
        return False

    def _get_container_state(self, container) -> str:
        if container.state.running:
            return "running"
        elif container.state.waiting:
            return f"waiting: {container.state.waiting.reason}"
        elif container.state.terminated:
            return f"terminated: {container.state.terminated.reason}"
        return "unknown"
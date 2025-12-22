import os
from typing import List, Union, Dict, Optional

try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
except ImportError:
    client = None
    config = None
    ApiException = Exception


class KubernetesClient:
    """
    A simple wrapper around the Kubernetes Python client to list pods,
    fetch pod logs, and inspect pod health.
    """

    def __init__(self, kube_config_path: Optional[str] = None):
        """
        Initialize the Kubernetes client.

        :param kube_config_path: Path to a kubeconfig file. If None, the default
                                 kubeconfig (~/.kube/config) is used.
        """
        if client is None or config is None:
            raise RuntimeError("kubernetes package is not installed")

        # Load kubeconfig
        if kube_config_path:
            if not os.path.exists(kube_config_path):
                raise FileNotFoundError(f"Kubeconfig not found: {kube_config_path}")
            config.load_kube_config(config_file=kube_config_path)
        else:
            config.load_kube_config()

        self.core_v1 = client.CoreV1Api()

    def list_pods(self, namespace: str = "default") -> Union[List[str], str, None]:
        """
        List pod names in the specified namespace.

        :param namespace: Kubernetes namespace.
        :return: List of pod names, or an error string, or None if no pods.
        """
        try:
            resp = self.core_v1.list_namespaced_pod(namespace=namespace)
            pod_names = [pod.metadata.name for pod in resp.items]
            return pod_names if pod_names else None
        except ApiException as exc:
            return f"Error listing pods: {exc}"
        except Exception as exc:
            return f"Unexpected error: {exc}"

    def get_pod_logs(self, pod_name: str, namespace: str = "default") -> Union[List[str], str]:
        """
        Retrieve logs for a specific pod.

        :param pod_name: Name of the pod.
        :param namespace: Kubernetes namespace.
        :return: List of log lines, or an error string.
        """
        try:
            log = self.core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                _preload_content=False,
            )
            # The API returns a stream; decode it.
            if isinstance(log, bytes):
                log_text = log.decode("utf-8")
            else:
                log_text = log
            return log_text.splitlines()
        except ApiException as exc:
            return f"Error fetching logs for pod '{pod_name}': {exc}"
        except Exception as exc:
            return f"Unexpected error: {exc}"

    def get_pod_health(self, pod_name: str, namespace: str = "default") -> Dict[str, Union[str, List[Dict]]]:
        """
        Inspect the health status of a pod.

        :param pod_name: Name of the pod.
        :param namespace: Kubernetes namespace.
        :return: Dictionary containing pod phase, conditions, and container statuses.
        """
        try:
            pod = self.core_v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            health = {
                "name": pod.metadata.name,
                "phase": pod.status.phase,
                "conditions": [
                    {
                        "type": cond.type,
                        "status": cond.status,
                        "reason": cond.reason,
                        "message": cond.message,
                    }
                    for cond in pod.status.conditions or []
                ],
                "container_statuses": [
                    {
                        "name": cs.name,
                        "state": cs.state.to_dict() if cs.state else None,
                        "ready": cs.ready,
                        "restart_count": cs.restart_count,
                        "image": cs.image,
                    }
                    for cs in pod.status.container_statuses or []
                ],
            }
            return health
        except ApiException as exc:
            return {"error": f"Error retrieving pod health: {exc}"}
        except Exception as exc:
            return {"error": f"Unexpected error: {exc}"}
from kubernetes import client, config
from ..utils import calculateAge, filter_annotations, configure_k8s

def get_role_binding_events(path, context, namespace, role_binding_name):
    configure_k8s(path, context)
    v1 = client.CoreV1Api()
    events = v1.list_namespaced_event(namespace=namespace).items
    role_binding_events = [
        event for event in events if event.involved_object.name == role_binding_name and event.involved_object.kind == "RoleBinding"
    ]

    return "\n".join([f"{e.reason}: {e.message}" for e in role_binding_events])
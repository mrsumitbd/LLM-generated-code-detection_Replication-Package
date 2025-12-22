from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_role_binding_events(path, context, namespace, role_binding_name):
    """
    Retrieve Kubernetes events related to a specific RoleBinding.

    Parameters
    ----------
    path : str
        Path to the kubeconfig file.
    context : str
        Name of the context to use from the kubeconfig.
    namespace : str
        Namespace where the RoleBinding resides.
    role_binding_name : str
        Name of the RoleBinding to filter events for.

    Returns
    -------
    list[client.V1Event]
        A list of V1Event objects that involve the specified RoleBinding.
    """
    # Load kubeconfig and set the desired context
    config.load_kube_config(config_file=path, context=context)

    v1 = client.CoreV1Api()

    try:
        # List all events in the namespace
        events = v1.list_namespaced_event(namespace=namespace)
    except ApiException as e:
        # If the namespace does not exist or another error occurs, return empty list
        return []

    # Filter events that involve the specified RoleBinding
    filtered_events = []
    for event in events.items:
        involved = event.involved_object
        if (
            involved.kind == "RoleBinding"
            and involved.name == role_binding_name
            and involved.namespace == namespace
        ):
            filtered_events.append(event)

    return filtered_events
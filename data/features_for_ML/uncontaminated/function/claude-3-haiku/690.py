import kubernetes
from kubernetes.client.rest import ApiException

def get_role_binding_events(path, context, namespace, role_binding_name):
    try:
        # Create a Kubernetes API client
        configuration = kubernetes.client.Configuration()
        configuration.host = path
        configuration.api_key = {'authorization': f'Bearer {context}'}
        api_client = kubernetes.client.ApiClient(configuration)

        # Get the RoleBinding object
        rbac_api = kubernetes.client.RbacAuthorizationV1Api(api_client)
        role_binding = rbac_api.read_namespaced_role_binding(role_binding_name, namespace)

        # Get the events for the RoleBinding
        core_api = kubernetes.client.CoreV1Api(api_client)
        events = core_api.list_namespaced_event(namespace, field_selector=f'involvedObject.name={role_binding.metadata.name}')

        return events.items
    except ApiException as e:
        print(f"Exception when calling Kubernetes API: {e}")
        return []
from .src.config_secrets import k8s_configmaps, k8s_secrets
from .src.cluster_management import k8s_namespaces, k8s_nodes, k8s_limit_range, k8s_resource_quota, k8s_pdb
from django.shortcuts import render

def secrets(request, cluster_id):
    cluster_id, current_cluster, path, registered_clusters, namespaces, context_name = get_utils_data(request)

    namespaces = k8s_namespaces.get_namespace(path, context_name)
    secrets, total_secrets = k8s_secrets.list_secrets(path, context_name)
    return render(request, 'dashboard/config_secrets/secrets.html', {"secrets": secrets, "total_secrets": total_secrets, "cluster_id": cluster_id, 
                                                                     'registered_clusters': registered_clusters, 'namespaces': namespaces, 'current_cluster': current_cluster})
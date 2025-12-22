import json
from typing import Any, Dict

# In‑memory store for secrets, keyed by cluster_id.
# Each cluster_id maps to a dict of secret_name -> secret_value.
_SECRETS_STORE: Dict[str, Dict[str, Any]] = {}


def secrets(request, cluster_id):
    """
    Handle CRUD operations for secrets belonging to a specific cluster.

    Supported HTTP methods:
        GET    - List all secret names for the cluster.
        POST   - Create a new secret. Expects JSON body with 'name' and 'value'.
        DELETE - Delete a secret by name. Expects query parameter 'name'.

    Parameters
    ----------
    request : object
        The request object. Must provide:
            - request.method (str)
            - request.args (dict-like for query parameters)
            - request.json (dict for POST body)
    cluster_id : str
        Identifier of the cluster whose secrets are being managed.

    Returns
    -------
    dict
        A JSON‑serializable dictionary containing the result of the operation.
    """
    # Ensure the cluster entry exists
    if cluster_id not in _SECRETS_STORE:
        _SECRETS_STORE[cluster_id] = {}

    cluster_secrets = _SECRETS_STORE[cluster_id]

    method = request.method.upper()

    if method == "GET":
        # Return a list of secret names
        return {
            "status": "success",
            "cluster_id": cluster_id,
            "secrets": list(cluster_secrets.keys()),
        }

    if method == "POST":
        # Create a new secret
        data = request.json or {}
        name = data.get("name")
        value = data.get("value")

        if not name or value is None:
            return {
                "status": "error",
                "message": "Both 'name' and 'value' must be provided.",
            }

        if name in cluster_secrets:
            return {
                "status": "error",
                "message": f"Secret '{name}' already exists.",
            }

        cluster_secrets[name] = value
        return {
            "status": "success",
            "message": f"Secret '{name}' created.",
            "cluster_id": cluster_id,
        }

    if method == "DELETE":
        # Delete a secret by name
        name = request.args.get("name")
        if not name:
            return {
                "status": "error",
                "message": "Query parameter 'name' is required for deletion.",
            }

        if name not in cluster_secrets:
            return {
                "status": "error",
                "message": f"Secret '{name}' not found.",
            }

        del cluster_secrets[name]
        return {
            "status": "success",
            "message": f"Secret '{name}' deleted.",
            "cluster_id": cluster_id,
        }

    # Unsupported method
    return {
        "status": "error",
        "message": f"Method '{method}' not allowed.",
    }
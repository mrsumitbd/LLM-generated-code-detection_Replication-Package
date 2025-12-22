import os
import requests
from typing import Optional

def list_schedules(
    sort_by: str = "desc:created",
    page: int = 1,
    size: int = 10,
    logical_operator: str = "and",
    created: Optional[str] = None,
    updated: Optional[str] = None,
    name: Optional[str] = None,
    pipeline_id: Optional[str] = None,
    orchestrator_id: Optional[str] = None,
    active: Optional[bool] = None,
) -> str:
    """
    List all schedules in the ZenML workspace.

    Args:
        sort_by: The field to sort the schedules by
        page: The page number to return
        size: The number of schedules to return
        logical_operator: Logical operator for filtering
        created: The creation date of the schedules
        updated: The last update date of the schedules
        name: The name of the schedules
        pipeline_id: The ID of the pipeline
        orchestrator_id: The ID of the orchestrator
        active: Whether the schedule is active

    Returns:
        str: The raw JSON response from the ZenML API.
    """
    base_url = os.getenv("ZENML_API_URL", "http://localhost:8000/api/v1")
    endpoint = f"{base_url}/schedules"

    params = {
        "sort_by": sort_by,
        "page": page,
        "size": size,
        "logical_operator": logical_operator,
    }

    # Optional filters
    if created is not None:
        params["created"] = created
    if updated is not None:
        params["updated"] = updated
    if name is not None:
        params["name"] = name
    if pipeline_id is not None:
        params["pipeline_id"] = pipeline_id
    if orchestrator_id is not None:
        params["orchestrator_id"] = orchestrator_id
    if active is not None:
        params["active"] = str(active).lower()

    try:
        response = requests.get(endpoint, params=params, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        # Return a JSON string with error details
        error_payload = {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None),
            "response_text": getattr(e.response, "text", None),
        }
        return str(error_payload)
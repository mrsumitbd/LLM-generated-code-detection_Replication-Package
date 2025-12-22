from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# The following imports are placeholders. In a real project these would be
# imported from the actual modules that define AgentACPDescriptor and
# AgentManifest.  They are defined here only so that the type checker does
# not complain when this file is imported in isolation.
try:
    from myproject.agent import AgentACPDescriptor, AgentManifest  # type: ignore
except Exception:  # pragma: no cover
    # Minimal stubs for type checking / documentation purposes
    class AgentACPDescriptor:  # pragma: no cover
        name: str
        description: str
        endpoints: List[Dict[str, Any]]

    class AgentManifest:  # pragma: no cover
        name: str
        description: str
        endpoints: List[Dict[str, Any]]


def _extract_endpoints(source: Any) -> List[Dict[str, Any]]:
    """
    Extract a list of endpoint definitions from the source object.

    Each endpoint definition is expected to be a mapping with at least the
    following keys:
        - path: The URL path (e.g. "/items")
        - method: The HTTP method (e.g. "GET", "POST")
        - summary: A short description of the operation
        - description: A longer description (optional)
        - parameters: A list of parameter definitions (optional)
        - responses: A mapping of status codes to response schemas (optional)

    If the source object does not provide an ``endpoints`` attribute, an empty
    list is returned.
    """
    if hasattr(source, "endpoints"):
        return list(source.endpoints)  # type: ignore
    return []


def _build_path_item(endpoint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a single endpoint definition into an OpenAPI path item.
    """
    method = endpoint.get("method", "get").lower()
    operation: Dict[str, Any] = {
        "summary": endpoint.get("summary", ""),
        "description": endpoint.get("description", ""),
        "operationId": endpoint.get("operationId", ""),
        "parameters": endpoint.get("parameters", []),
        "responses": endpoint.get("responses", {"200": {"description": "Success"}}),
    }
    return {method: operation}


def _build_paths(endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build the ``paths`` section of an OpenAPI document from a list of
    endpoint definitions.
    """
    paths: Dict[str, Any] = {}
    for ep in endpoints:
        path = ep.get("path", "/")
        paths.setdefault(path, {}).update(_build_path_item(ep))
    return paths


def _build_info(source: Any) -> Dict[str, Any]:
    """
    Build the ``info`` section of an OpenAPI document.
    """
    return {
        "title": getattr(source, "name", "Agent API"),
        "description": getattr(source, "description", ""),
        "version": getattr(source, "version", "1.0.0"),
    }


def generate_agent_oapi(
    agent_source: Union[AgentACPDescriptor, AgentManifest],
    spec_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate an OpenAPI 3.0 specification for an agent.

    Parameters
    ----------
    agent_source : Union[AgentACPDescriptor, AgentManifest]
        The source object that contains the agent metadata and endpoint
        definitions.  The object must expose at least the following
        attributes:
            - ``name`` (str): The name of the agent.
            - ``description`` (str): A short description.
            - ``endpoints`` (Iterable[Mapping]): A collection of endpoint
              definitions.  Each endpoint definition is a mapping that
              contains the keys ``path`` and ``method`` at a minimum.
    spec_path : Optional[str], default None
        If provided, the generated OpenAPI document will be written to the
        given file path in JSON format.  The directory will be created if it
        does not exist.

    Returns
    -------
    Dict[str, Any]
        The OpenAPI document as a Python dictionary.
    """
    # Extract endpoints
    endpoints = _extract_endpoints(agent_source)

    # Build the OpenAPI document
    openapi_doc: Dict[str, Any] = {
        "openapi": "3.0.0",
        "info": _build_info(agent_source),
        "paths": _build_paths(endpoints),
    }

    # Write to file if requested
    if spec_path:
        path_obj = Path(spec_path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        with path_obj.open("w", encoding="utf-8") as fp:
            json.dump(openapi_doc, fp, indent=2, sort_keys=True)

    return openapi_doc
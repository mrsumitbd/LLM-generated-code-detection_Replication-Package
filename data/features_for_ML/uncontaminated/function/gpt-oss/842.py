import dataclasses
from typing import Any

def _node_to_data(node: "DAGNode") -> "FlowNodeData":
    """
    Convert a DAGNode instance into a FlowNodeData instance.

    The conversion is performed by mapping attributes of the node to the
    corresponding fields of FlowNodeData.  If FlowNodeData is a dataclass,
    its fields are inspected via dataclasses.fields.  If it is a Pydantic
    model or any other mapping‑compatible type, the same approach works
    because the constructor accepts keyword arguments.

    Parameters
    ----------
    node : DAGNode
        The node to convert.

    Returns
    -------
    FlowNodeData
        A new FlowNodeData instance populated with data from the node.
    """
    # Prepare a dictionary of keyword arguments for FlowNodeData.
    kwargs: dict[str, Any] = {}

    # Try to introspect FlowNodeData as a dataclass first.
    try:
        for field in dataclasses.fields(FlowNodeData):
            kwargs[field.name] = getattr(node, field.name, None)
    except TypeError:
        # If FlowNodeData is not a dataclass, fall back to a generic
        # attribute lookup using its __dict__ or __slots__.
        # We attempt to use the node's __dict__ if available.
        if hasattr(node, "__dict__"):
            for key, value in node.__dict__.items():
                kwargs[key] = value
        else:
            # As a last resort, use dir() to find attributes that are not
            # private or built‑in.
            for key in dir(node):
                if key.startswith("_"):
                    continue
                try:
                    value = getattr(node, key)
                except Exception:
                    continue
                kwargs[key] = value

    # Instantiate FlowNodeData with the collected keyword arguments.
    return FlowNodeData(**kwargs)
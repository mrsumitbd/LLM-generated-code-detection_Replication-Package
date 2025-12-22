def _node_to_data(node: DAGNode) -> FlowNodeData:
    """Convert a DAGNode to FlowNodeData."""
    return FlowNodeData(
        id=node.id,
        label=node.label,
        type=node.type,
        data=node.data,
        position=node.position,
        style=node.style,
        selected=node.selected,
        dragging=node.dragging,
        hidden=node.hidden,
        parent_id=node.parent_id,
        extent=node.extent,
        expandParent=node.expand_parent,
        positionAbsolute=node.position_absolute,
        ariaLabel=node.aria_label,
        focusable=node.focusable,
        draggable=node.draggable,
        selectable=node.selectable,
        connectable=node.connectable,
        deletable=node.deletable,
        zIndex=node.z_index,
    )
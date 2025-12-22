def _node_to_data(node: DAGNode) -> FlowNodeData:
    return FlowNodeData(
        id=node.id,
        type=node.type,
        label=node.label,
        description=node.description,
        inputs=node.inputs,
        outputs=node.outputs,
        parameters=node.parameters,
        configuration=node.configuration,
        metadata=node.metadata
    )
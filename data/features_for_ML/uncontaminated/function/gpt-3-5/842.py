def _node_to_data(node: DAGNode) -> FlowNodeData:
    data = FlowNodeData()
    data.id = node.id
    data.name = node.name
    data.inputs = node.inputs
    data.outputs = node.outputs
    return data
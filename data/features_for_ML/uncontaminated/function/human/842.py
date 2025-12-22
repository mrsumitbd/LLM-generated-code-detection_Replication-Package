from derisk.core.awel.flow.flow_factory import FlowPanel, FlowCategory, State, FlowData, FlowPositionData, FlowNodeData, FlowEdgeData
from derisk.core.awel.dag.base import DAGNode

def _node_to_data(node: DAGNode) -> FlowNodeData:
    return FlowNodeData(
        width=320,
        height=320,
        id=node.metadata.id,
        position=FlowPositionData(x=0, y=0, zoom=0),
        position_absolute=FlowPositionData(x=0, y=0, zoom=0),
        type="customNode",
        data=node.metadata
    )
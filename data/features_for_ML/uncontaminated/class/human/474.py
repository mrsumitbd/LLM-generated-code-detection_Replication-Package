import xax
from jaxtyping import Array, PyTree

class PhysicsState:
    """Everything you need for the engine to take an action and step physics."""

    last_ctrl: Array
    data: PhysicsData
    event_states: xax.FrozenDict[str, PyTree]
    actuator_state: PyTree
    action_latency: Array
    zero_offset: Array
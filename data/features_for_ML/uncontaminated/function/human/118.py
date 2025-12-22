from typing import Any, Dict, List, Tuple, Type

def world_state_from_bytes(b: bytes, i: int) -> Tuple[WorldState, int]:
    environment_states, i = _from_bytes(b, i)
    opponent_states, i = _from_bytes(b, i)
    personal_states, i = _from_bytes(b, i)
    return WorldState(environment_states=environment_states, opponent_states=opponent_states, personal_states=personal_states), i
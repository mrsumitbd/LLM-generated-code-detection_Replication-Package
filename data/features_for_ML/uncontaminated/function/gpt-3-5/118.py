from typing import Tuple

class WorldState:
    def __init__(self, data):
        self.data = data

def world_state_from_bytes(b: bytes, i: int) -> Tuple[WorldState, int]:
    data = b[i:i+4]
    i += 4
    return WorldState(data), i
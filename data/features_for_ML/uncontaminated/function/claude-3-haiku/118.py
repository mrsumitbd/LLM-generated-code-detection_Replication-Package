from typing import Tuple
from dataclasses import dataclass

@dataclass
class WorldState:
    x: int
    y: int
    z: int

def world_state_from_bytes(b: bytes, i: int) -> Tuple[WorldState, int]:
    x = int.from_bytes(b[i:i+4], byteorder='little', signed=True)
    y = int.from_bytes(b[i+4:i+8], byteorder='little', signed=True)
    z = int.from_bytes(b[i+8:i+12], byteorder='little', signed=True)
    return WorldState(x, y, z), i + 12
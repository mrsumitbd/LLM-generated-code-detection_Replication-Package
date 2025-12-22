from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import List, Tuple

# Try to import the real WorldState and ObjectState classes if they exist.
# If they are not available, fall back to simple dataclass definitions
# that match the expected interface.

try:
    from .world_state import WorldState  # type: ignore
except Exception:  # pragma: no cover
    @dataclass
    class WorldState:
        timestamp: float
        objects: List["ObjectState"]  # type: ignore

try:
    from .object_state import ObjectState  # type: ignore
except Exception:  # pragma: no cover
    @dataclass
    class ObjectState:
        id: int
        type: int
        position: Tuple[float, float, float]
        velocity: Tuple[float, float, float]


def world_state_from_bytes(b: bytes, i: int) -> Tuple[WorldState, int]:
    """
    Parse a WorldState from a byte buffer starting at index `i`.

    The binary format is defined as follows (little‑endian):

    * 8 bytes  – timestamp (double)
    * 4 bytes  – number of objects (unsigned int)
    * For each object:
        * 4 bytes  – object id (unsigned int)
        * 1 byte   – object type (unsigned char)
        * 3 bytes  – padding (ignored)
        * 12 bytes – position (3 floats)
        * 12 bytes – velocity (3 floats)

    Returns a tuple of the parsed WorldState and the new index after the
    parsed data.
    """
    # Read timestamp
    timestamp, = struct.unpack_from("<d", b, i)
    i += 8

    # Read number of objects
    num_objects, = struct.unpack_from("<I", b, i)
    i += 4

    objects: List[ObjectState] = []

    for _ in range(num_objects):
        # Object id
        obj_id, = struct.unpack_from("<I", b, i)
        i += 4

        # Object type
        obj_type, = struct.unpack_from("<B", b, i)
        i += 1

        # Skip 3 padding bytes
        i += 3

        # Position (x, y, z)
        x, y, z = struct.unpack_from("<fff", b, i)
        i += 12

        # Velocity (vx, vy, vz)
        vx, vy, vz = struct.unpack_from("<fff", b, i)
        i += 12

        objects.append(ObjectState(obj_id, obj_type, (x, y, z), (vx, vy, vz)))

    world_state = WorldState(timestamp, objects)
    return world_state, i
import torch.distributed as dist
import os

def get_machine_format() -> str:
    node_id = os.environ.get("NGC_ARRAY_INDEX", "0")
    num_nodes = int(os.environ.get("NGC_ARRAY_SIZE", "1"))
    machine_format = ""
    rank = 0
    if dist.is_available():
        if not RANK0_ONLY and dist.is_initialized():
            rank = dist.get_rank()
            world_size = dist.get_world_size()
            machine_format = (
                f"<red>[Node{node_id:<3}/{num_nodes:<3}][RANK{rank:<5}/{world_size:<5}]" + "[{process.name:<8}]</red>| "
            )
    return machine_format
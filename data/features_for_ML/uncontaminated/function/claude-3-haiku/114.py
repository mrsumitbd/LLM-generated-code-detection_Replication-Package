import os
import torch.distributed as dist

def get_nccl_id_store_by_name(name):
    if not dist.is_available() or not dist.is_initialized():
        return None

    store = dist.distributed_c10d._get_default_store()
    if store is None:
        return None

    key = f"nccl_id_{name}"
    if store.has_key(key):
        return store.get(key)
    else:
        return None
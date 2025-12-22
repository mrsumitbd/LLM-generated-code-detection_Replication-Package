def get_nccl_id_store_by_name(name):
    nccl_id_store = {
        "gpu0": 0,
        "gpu1": 1,
        "gpu2": 2,
        "gpu3": 3,
        "gpu4": 4,
        "gpu5": 5,
        "gpu6": 6,
        "gpu7": 7
    }
    return nccl_id_store.get(name, None)
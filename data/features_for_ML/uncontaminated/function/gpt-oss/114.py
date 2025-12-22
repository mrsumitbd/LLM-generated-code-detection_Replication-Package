import threading

# Global registry for NCCL ID stores keyed by name.
_nccl_id_stores = {}
_registry_lock = threading.Lock()


def get_nccl_id_store_by_name(name):
    """
    Retrieve (or create) an NCCL ID store identified by `name`.

    The store is a simple in‑memory dictionary that can be used to
    exchange NCCL IDs between processes.  The function is thread‑safe
    and guarantees that the same store instance is returned for a
    given name.

    Parameters
    ----------
    name : str
        Identifier for the NCCL ID store.

    Returns
    -------
    dict
        The store associated with the given name.
    """
    with _registry_lock:
        if name not in _nccl_id_stores:
            _nccl_id_stores[name] = {}
        return _nccl_id_stores[name]
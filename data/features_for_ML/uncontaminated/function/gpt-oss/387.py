def temporal_data_to_data(data: CollatableTemporalData) -> Data:
    """
    NeighborLoader requires a `Data` object.
    We need to convert `CollatableTemporalData` to `Data` before using it.
    """
    import torch
    from torch_geometric.data import Data

    def is_tensor_list(obj):
        return isinstance(obj, list) and all(isinstance(t, torch.Tensor) for t in obj)

    # Handle list of Data objects
    if isinstance(data, list):
        cum_nodes = 0
        edge_indices = []
        attrs = {}
        for d in data:
            for key, val in d.__dict__.items():
                if key.startswith("_"):
                    continue
                if key == "edge_index":
                    edge_indices.append(val + cum_nodes)
                else:
                    attrs.setdefault(key, []).append(val)
            cum_nodes += d.num_nodes
        for key, vals in attrs.items():
            attrs[key] = torch.cat(vals, dim=0)
        attrs["edge_index"] = torch.cat(edge_indices, dim=1)
        return Data(**attrs)

    # Handle CollatableTemporalData
    attrs = {}
    cum_nodes = 0
    edge_indices = []
    node_counts = None
    if hasattr(data, "num_nodes"):
        node_counts = data.num_nodes
        if isinstance(node_counts, list):
            node_counts = list(node_counts)
        else:
            node_counts = [node_counts]

    for attr_name in dir(data):
        if attr_name.startswith("_"):
            continue
        val = getattr(data, attr_name)
        if is_tensor_list(val):
            if attr_name == "edge_index":
                for ei, n_nodes in zip(val, node_counts or []):
                    edge_indices.append(ei + cum_nodes)
                    cum_nodes += n_nodes
            else:
                attrs[attr_name] = torch.cat(val, dim=0)
        elif isinstance(val, torch.Tensor):
            attrs[attr_name] = val

    if edge_indices:
        attrs["edge_index"] = torch.cat(edge_indices, dim=1)
    return Data(**attrs)
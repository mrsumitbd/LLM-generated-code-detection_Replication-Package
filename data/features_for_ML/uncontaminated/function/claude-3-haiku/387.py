def temporal_data_to_data(data: CollatableTemporalData) -> Data:
    """
    NeighborLoader requires a `Data` object.
    We need to convert `CollatableTemporalData` to `Data` before using it.
    """
    x = data.x
    edge_index = data.edge_index
    edge_attr = data.edge_attr
    y = data.y
    time = data.time
    return Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y, time=time)
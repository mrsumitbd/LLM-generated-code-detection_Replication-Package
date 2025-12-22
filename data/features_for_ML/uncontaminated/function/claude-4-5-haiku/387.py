def temporal_data_to_data(data: CollatableTemporalData) -> Data:
    """
    NeighborLoader requires a `Data` object.
    We need to convert `CollatableTemporalData` to `Data` before using it.
    """
    from torch_geometric.data import Data
    
    # Extract the underlying data from CollatableTemporalData
    # CollatableTemporalData wraps temporal data, we need to convert it to standard Data
    data_dict = {}
    
    # Copy all attributes from the temporal data to the data dictionary
    for key, value in data:
        data_dict[key] = value
    
    # Create and return a Data object with the extracted attributes
    return Data(**data_dict)
def temporal_data_to_data(data: CollatableTemporalData) -> Data:
    return Data(data.data, data.targets)
def execute(
    data: Dict[str, pa.Table], config: U256ToBinaryConfig
) -> Dict[str, pa.Table]:
    result = {}
    for key, table in data.items():
        new_table = table.select([
            table.column(col) for col in table.column_names
        ]).apply(
            lambda row: U256ToBinary(row, config),
            output_types=[col.type for col in table.schema],
        )
        result[key] = new_table
    return result

def U256ToBinary(row, config: U256ToBinaryConfig):
    values = []
    for col in row:
        if isinstance(col, int):
            values.append(bin(col)[2:].zfill(config.bits))
        else:
            values.append(col)
    return tuple(values)
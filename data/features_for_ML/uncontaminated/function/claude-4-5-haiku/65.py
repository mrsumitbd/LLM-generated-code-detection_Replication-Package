def execute(
    data: Dict[str, pa.Table], config: U256ToBinaryConfig
) -> Dict[str, pa.Table]:
    import pyarrow as pa
    import pyarrow.compute as pc
    
    result = {}
    
    for table_name, table in data.items():
        columns = {}
        
        for col_name in table.column_names:
            column = table[col_name]
            
            if col_name in config.columns:
                # Convert U256 (represented as large integers) to binary string
                def u256_to_binary(val):
                    if val is None:
                        return None
                    # Convert integer to binary string without '0b' prefix
                    return bin(int(val))[2:]
                
                # Apply the conversion
                binary_column = pc.list_element(
                    pc.list_parent_indices(column),
                    0
                )
                
                # Use pyarrow's compute functions to convert
                try:
                    # Try to cast to int64 first, then convert
                    int_col = pc.cast(column, pa.int64())
                    binary_strs = pc.binary_join_element_wise(
                        pc.cast(int_col, pa.string()),
                        ""
                    )
                except:
                    # Fallback: handle as string and convert
                    binary_strs = pc.cast(column, pa.string())
                
                # Create binary representation
                def convert_to_binary(x):
                    if x is None or x == "":
                        return None
                    try:
                        num = int(x) if isinstance(x, str) else x
                        return bin(num)[2:]
                    except:
                        return None
                
                binary_array = pa.array([
                    convert_to_binary(val.as_py()) if val.is_valid else None
                    for val in column
                ], type=pa.string())
                
                columns[col_name] = binary_array
            else:
                columns[col_name] = column
        
        result[table_name] = pa.table(columns)
    
    return result
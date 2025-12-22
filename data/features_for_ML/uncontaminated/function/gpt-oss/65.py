import pyarrow as pa
from typing import Dict, Any

# Assuming the config object has these attributes.
# If the actual config class differs, adjust attribute names accordingly.
class U256ToBinaryConfig:
    input_column: str
    output_column: str
    bit_width: int

def execute(
    data: Dict[str, pa.Table], config: U256ToBinaryConfig
) -> Dict[str, pa.Table]:
    """
    Convert a column containing 256‑bit unsigned integers to a binary string
    representation.

    Parameters
    ----------
    data : Dict[str, pa.Table]
        Mapping from table names to pyarrow tables.
    config : U256ToBinaryConfig
        Configuration specifying the input column name, the output column name,
        and the desired bit width for the binary representation.

    Returns
    -------
    Dict[str, pa.Table]
        New mapping with the same keys, where each table has an additional
        column containing the binary string representation of the input column.
    """
    input_col = getattr(config, "input_column")
    output_col = getattr(config, "output_column")
    bit_width = getattr(config, "bit_width")

    result: Dict[str, pa.Table] = {}

    for name, table in data.items():
        if input_col not in table.column_names:
            # If the input column is missing, keep the table unchanged.
            result[name] = table
            continue

        # Extract the column as a list of values.
        col_values = table[input_col].to_pylist()

        # Convert each value to a binary string of the specified width.
        binary_values = []
        for v in col_values:
            if v is None:
                binary_values.append(None)
            else:
                # Accept int, string (decimal or hex), or bytes.
                if isinstance(v, int):
                    num = v
                elif isinstance(v, str):
                    # Try hex first, then decimal.
                    try:
                        num = int(v, 16)
                    except ValueError:
                        num = int(v)
                elif isinstance(v, bytes):
                    num = int.from_bytes(v, byteorder="big")
                else:
                    # Unsupported type: keep null.
                    num = None

                if num is None:
                    binary_values.append(None)
                else:
                    # Ensure non-negative and within bit width.
                    if num < 0:
                        raise ValueError(f"Negative value {num} in column {input_col}")
                    if num >= 1 << bit_width:
                        raise ValueError(
                            f"Value {num} exceeds the configured bit width {bit_width}"
                        )
                    binary_str = format(num, "b").zfill(bit_width)
                    binary_values.append(binary_str)

        # Create a new column with the binary strings.
        binary_array = pa.array(binary_values, type=pa.string())
        new_table = table.append_column(output_col, binary_array)
        result[name] = new_table

    return result
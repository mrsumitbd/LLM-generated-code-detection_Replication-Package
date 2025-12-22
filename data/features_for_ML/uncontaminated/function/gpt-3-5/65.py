from typing import Dict
import pyarrow as pa

class U256ToBinaryConfig:
    def __init__(self, threshold: int):
        self.threshold = threshold

def execute(
    data: Dict[str, pa.Table], config: U256ToBinaryConfig
) -> Dict[str, pa.Table]:
    result = {}
    for key, table in data.items():
        result[key] = pa.Table.from_pandas(table.to_pandas().applymap(lambda x: 1 if x >= config.threshold else 0))
    return result
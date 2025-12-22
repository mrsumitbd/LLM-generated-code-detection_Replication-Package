import re
from typing import Tuple

def parse_node(line: str) -> Tuple:
    """
    Parse a line of the execution plan to extract node id and node name.
    Example: '* ShuffleQueryStage (11), Statistics(sizeInBytes=1669.9 MiB)' is parsed to (11, 'ShuffleQueryStage')
    """
    pattern = r'\* (\w+) \((\d+)\)'
    match = re.search(pattern, line)
    if match:
        node_name = match.group(1)
        node_id = int(match.group(2))
        return (node_id, node_name)
    else:
        return (None, None)
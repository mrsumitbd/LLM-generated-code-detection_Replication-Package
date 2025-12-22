import re
from typing import Tuple

def parse_node(line: str) -> Tuple[int, str]:
    """
    Parse a line of the execution plan to extract node id and node name.

    Example:
        '* ShuffleQueryStage (11), Statistics(sizeInBytes=1669.9 MiB)'
        -> (11, 'ShuffleQueryStage')
    """
    # Regular expression to capture the node name and id.
    # It allows an optional leading '*', any whitespace, then the node name
    # (non-greedy), optional whitespace, then the id in parentheses.
    pattern = r'^\s*\*?\s*(.*?)\s*\((\d+)\)'
    match = re.match(pattern, line)
    if not match:
        raise ValueError(f"Line does not contain a valid node id: {line!r}")

    node_name, node_id_str = match.groups()
    node_name = node_name.strip()
    node_id = int(node_id_str)
    return node_id, node_name
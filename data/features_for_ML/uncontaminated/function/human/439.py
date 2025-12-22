from typing import Dict, List, Tuple
import re

def parse_node(line: str) -> Tuple:
    '''
    Parse a line of the execution plan to extract node id and node name.
    Example: '* ShuffleQueryStage (11), Statistics(sizeInBytes=1669.9 MiB)' is parsed to (11, 'ShuffleQueryStage')
    '''
    int_match = re.search(r'\((\d+)\)', line)  # Match the number in parentheses
    node_id = int(int_match.group(1)) if int_match else None

    name_match = re.search(r"[a-zA-Z0-9][a-zA-Z0-9\s]*?(?=\s*\()", line)  # First alphanumeric string before '('
    node_name = name_match.group(0).strip() if name_match else None
    return node_id, node_name
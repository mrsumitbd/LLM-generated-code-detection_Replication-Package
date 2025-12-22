from typing import Tuple

def parse_node(line: str) -> Tuple:
    start = line.find('(')
    end = line.find(')')
    node_id = int(line[start+1:end])
    node_name = line.split()[1]
    return (node_id, node_name)
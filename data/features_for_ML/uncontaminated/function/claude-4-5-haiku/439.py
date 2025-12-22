def parse_node(line: str) -> Tuple:
    '''
    Parse a line of the execution plan to extract node id and node name.
    Example: '* ShuffleQueryStage (11), Statistics(sizeInBytes=1669.9 MiB)' is parsed to (11, 'ShuffleQueryStage')
    '''
    import re
    
    # Remove leading asterisk and whitespace
    line = line.lstrip('* ')
    
    # Extract node name (everything before the first opening parenthesis)
    node_name_match = re.match(r'([^\(]+)', line)
    if not node_name_match:
        return None
    
    node_name = node_name_match.group(1).strip()
    
    # Extract node id from parentheses
    id_match = re.search(r'\((\d+)\)', line)
    if not id_match:
        return None
    
    node_id = int(id_match.group(1))
    
    return (node_id, node_name)
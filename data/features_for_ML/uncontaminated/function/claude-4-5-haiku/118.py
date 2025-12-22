def world_state_from_bytes(b: bytes, i: int) -> Tuple[WorldState, int]:
    """Parse a WorldState object from bytes starting at index i."""
    # Parse version
    version = int.from_bytes(b[i:i+4], byteorder='little')
    i += 4
    
    # Parse block height
    block_height = int.from_bytes(b[i:i+8], byteorder='little')
    i += 8
    
    # Parse timestamp
    timestamp = int.from_bytes(b[i:i+8], byteorder='little')
    i += 8
    
    # Parse number of accounts
    num_accounts = int.from_bytes(b[i:i+4], byteorder='little')
    i += 4
    
    # Parse accounts
    accounts = {}
    for _ in range(num_accounts):
        # Parse account address length
        addr_len = int.from_bytes(b[i:i+2], byteorder='little')
        i += 2
        
        # Parse account address
        address = b[i:i+addr_len].decode('utf-8')
        i += addr_len
        
        # Parse account balance
        balance = int.from_bytes(b[i:i+8], byteorder='little')
        i += 8
        
        # Parse account nonce
        nonce = int.from_bytes(b[i:i+8], byteorder='little')
        i += 8
        
        accounts[address] = {'balance': balance, 'nonce': nonce}
    
    # Parse number of contracts
    num_contracts = int.from_bytes(b[i:i+4], byteorder='little')
    i += 4
    
    # Parse contracts
    contracts = {}
    for _ in range(num_contracts):
        # Parse contract address length
        addr_len = int.from_bytes(b[i:i+2], byteorder='little')
        i += 2
        
        # Parse contract address
        address = b[i:i+addr_len].decode('utf-8')
        i += addr_len
        
        # Parse contract code length
        code_len = int.from_bytes(b[i:i+4], byteorder='little')
        i += 4
        
        # Parse contract code
        code = b[i:i+code_len]
        i += code_len
        
        contracts[address] = code
    
    # Create WorldState object
    world_state = WorldState(
        version=version,
        block_height=block_height,
        timestamp=timestamp,
        accounts=accounts,
        contracts=contracts
    )
    
    return world_state, i
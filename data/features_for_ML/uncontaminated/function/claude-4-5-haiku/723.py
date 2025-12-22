def save_indexid2msg(indexid2msg, split2nodes, cfg):
    """
    The saving must occur after the graph construction, because some edge types
    are not considered and this results in some nodes that are not used in the pipeline.
    These nodes must be removed before storing to disk to avoid future errors.
    """
    import os
    import pickle
    
    # Collect all nodes that are actually used in the pipeline
    used_nodes = set()
    for split, nodes in split2nodes.items():
        used_nodes.update(nodes)
    
    # Filter indexid2msg to only include used nodes
    filtered_indexid2msg = {
        idx: msg for idx, msg in indexid2msg.items() 
        if idx in used_nodes
    }
    
    # Create output directory if it doesn't exist
    output_dir = cfg.get('output_dir', '.')
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine output path
    output_path = os.path.join(output_dir, 'indexid2msg.pkl')
    
    # Save the filtered mapping to disk
    with open(output_path, 'wb') as f:
        pickle.dump(filtered_indexid2msg, f)
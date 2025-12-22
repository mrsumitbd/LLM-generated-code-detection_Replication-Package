def save_indexid2msg(indexid2msg, split2nodes, cfg):
    """
    The saving must occur after the graph construction, because some edge types
    are not considered and this results in some nodes that are not used in the pipeline.
    These nodes must be removed before storing to disk to avoid future errors.
    """
    # Create a set of used nodes
    used_nodes = set()
    for split, nodes in split2nodes.items():
        used_nodes.update(nodes)

    # Create a new dictionary with only the used nodes
    new_indexid2msg = {k: v for k, v in indexid2msg.items() if k in used_nodes}

    # Save the new dictionary to disk
    with open(cfg.indexid2msg_path, 'wb') as f:
        pickle.dump(new_indexid2msg, f)
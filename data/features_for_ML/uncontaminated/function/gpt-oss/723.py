import json
import os

def save_indexid2msg(indexid2msg, split2nodes, cfg):
    """
    The saving must occur after the graph construction, because some edge types
    are not considered and this results in some nodes that are not used in the pipeline.
    These nodes must be removed before storing to disk to avoid future errors.
    """
    # Collect all node ids that are actually used in the pipeline
    used_ids = set()
    for nodes in split2nodes.values():
        used_ids.update(nodes)

    # Filter the indexid2msg dictionary to keep only used nodes
    filtered_indexid2msg = {k: v for k, v in indexid2msg.items() if k in used_ids}

    # Determine the output path
    # Prefer an explicit path in cfg, otherwise fall back to a default location
    output_path = getattr(cfg, "indexid2msg_path", None)
    if output_path is None:
        output_dir = getattr(cfg, "output_dir", ".")
        output_path = os.path.join(output_dir, "indexid2msg.json")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the filtered mapping to disk as JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_indexid2msg, f, ensure_ascii=False, indent=2)

    return output_path
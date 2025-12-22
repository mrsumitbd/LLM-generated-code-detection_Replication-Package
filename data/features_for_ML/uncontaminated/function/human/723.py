import os
import torch
from pidsmaker.utils.utils import (
    datetime_to_ns_time_US,
    get_split_to_files,
    init_database_connection,
    log,
    log_start,
    log_tqdm,
    ns_time_to_datetime_US,
    stringtomd5,
)

def save_indexid2msg(indexid2msg, split2nodes, cfg):
    """
    The saving must occur after the graph construction, because some edge types
    are not considered and this results in some nodes that are not used in the pipeline.
    These nodes must be removed before storing to disk to avoid future errors.
    """
    all_nodes = set().union(*(split2nodes[split] for split in ["train", "val", "test"]))
    indexid2msg = {k: v for k, v in indexid2msg.items() if k in all_nodes}

    out_dir = cfg.preprocessing.build_graphs._dicts_dir
    os.makedirs(out_dir, exist_ok=True)
    log("Saving indexid2msg to disk...")
    torch.save(indexid2msg, os.path.join(out_dir, "indexid2msg.pkl"))
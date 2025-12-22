def save_indexid2msg(indexid2msg, split2nodes, cfg):
    filtered_indexid2msg = {index_id: msg for index_id, msg in indexid2msg.items() if index_id in split2nodes[cfg['split']]}
    
    with open(cfg['output_file'], 'w') as f:
        for index_id, msg in filtered_indexid2msg.items():
            f.write(f"{index_id}\t{msg}\n")
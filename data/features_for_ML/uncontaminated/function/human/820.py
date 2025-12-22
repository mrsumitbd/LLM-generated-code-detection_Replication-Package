def guess_block_id(name):
            names = name.split("_")
            for i in names:
                if i.isdigit():
                    return i, name.replace(f"_{i}_", "_blockid_")
            return None, None
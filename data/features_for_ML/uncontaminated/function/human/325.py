import re

def _is_c_file(path) -> bool:
    lang_type = re.compile(r"\.(h|c|hpp|cc|cpp|cu|go|cuh|proto)$")
    if lang_type.search(path) is not None:
        return True
    return False
def _parse_from_test_patch(test_patch: str, func_name: str) -> str:
    start_index = test_patch.find(func_name)
    if start_index == -1:
        return ""
    
    start_index = test_patch.find("(", start_index)
    if start_index == -1:
        return ""
    
    end_index = test_patch.find(")", start_index)
    if end_index == -1:
        return ""
    
    return test_patch[start_index + 1:end_index]
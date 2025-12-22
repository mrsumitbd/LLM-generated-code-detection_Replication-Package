def _parse_from_test_patch(test_patch: str, func_name: str) -> str:
    start_marker = f"def {func_name}("
    end_marker = f")\n"
    
    start_index = test_patch.index(start_marker) + len(start_marker)
    end_index = test_patch.index(end_marker, start_index)
    
    return test_patch[start_index:end_index]
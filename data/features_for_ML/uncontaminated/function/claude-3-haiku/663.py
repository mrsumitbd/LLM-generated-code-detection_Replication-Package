def get_current_displayed_files(self) -> List[Dict[str, Any]]:
    """
    Get the currently displayed files (after filtering).
    
    Returns:
        List of currently displayed file dictionaries
    """
    displayed_files = []
    for file in self.all_files:
        if self.is_file_displayed(file):
            displayed_files.append(file.to_dict())
    return displayed_files
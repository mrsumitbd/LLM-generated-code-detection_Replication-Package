from typing import List, Dict, Any, Optional

def get_current_displayed_files(self) -> List[Dict[str, Any]]:
        """
        Get the currently displayed files (after filtering).
        
        Returns:
            List of currently displayed file dictionaries
        """
        if hasattr(self, 'filtered_files_data'):
            return self.filtered_files_data.copy()
        elif hasattr(self, 'displayed_files_details'):
            return self.displayed_files_details.copy()
        else:
            return []
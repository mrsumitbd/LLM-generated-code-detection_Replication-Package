def find_and_replace_pattern_with_aow_and_update_counters():
    """
    Find and replace patterns with 'aow' and update counters.
    This function demonstrates pattern matching and replacement with counter updates.
    """
    import re
    
    def process_text(text, pattern, replacement='aow'):
        """
        Find all occurrences of a pattern and replace them while tracking counts.
        
        Args:
            text: Input text to process
            pattern: Regex pattern to find
            replacement: Replacement string (default: 'aow')
            
        Returns:
            Tuple of (modified_text, replacement_count, pattern_count)
        """
        if not isinstance(text, str):
            return text, 0, 0
        
        # Find all matches
        matches = list(re.finditer(pattern, text))
        pattern_count = len(matches)
        
        # Replace all occurrences
        modified_text = re.sub(pattern, replacement, text)
        replacement_count = pattern_count
        
        return modified_text, replacement_count, pattern_count
    
    # Example usage with common patterns
    counters = {
        'replacements': 0,
        'patterns_found': 0,
        'total_operations': 0
    }
    
    def update_counters(replacement_count, pattern_count):
        """Update global counters based on operation results."""
        counters['replacements'] += replacement_count
        counters['patterns_found'] += pattern_count
        counters['total_operations'] += 1
        return counters
    
    # Return the processing function and counter update function
    return {
        'process': process_text,
        'update_counters': update_counters,
        'get_counters': lambda: counters,
        'reset_counters': lambda: counters.update({
            'replacements': 0,
            'patterns_found': 0,
            'total_operations': 0
        })
    }
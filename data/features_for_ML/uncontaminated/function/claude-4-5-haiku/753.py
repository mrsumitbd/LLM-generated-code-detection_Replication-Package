def preprocess(examples):
    """
    Preprocess examples for machine learning tasks.
    This is a generic preprocessing function that handles common text preprocessing tasks.
    """
    if not examples:
        return examples
    
    # Handle dictionary input (common in HuggingFace datasets)
    if isinstance(examples, dict):
        processed = {}
        for key, values in examples.items():
            if isinstance(values, list):
                processed[key] = [preprocess_text(v) if isinstance(v, str) else v for v in values]
            else:
                processed[key] = preprocess_text(values) if isinstance(values, str) else values
        return processed
    
    # Handle list input
    elif isinstance(examples, list):
        return [preprocess_text(ex) if isinstance(ex, str) else ex for ex in examples]
    
    # Handle string input
    elif isinstance(examples, str):
        return preprocess_text(examples)
    
    return examples


def preprocess_text(text):
    """
    Helper function to preprocess individual text strings.
    """
    if not isinstance(text, str):
        return text
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text
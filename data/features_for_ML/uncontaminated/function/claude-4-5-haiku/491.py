def preprocess(sample, is_cot=False):
    """
    Preprocess a sample for model training/inference.
    
    Args:
        sample: A dictionary containing 'question' and optionally 'answer' keys
        is_cot: Boolean flag indicating if chain-of-thought processing is needed
    
    Returns:
        A preprocessed dictionary with formatted text
    """
    if not isinstance(sample, dict):
        raise ValueError("Sample must be a dictionary")
    
    question = sample.get('question', '').strip()
    answer = sample.get('answer', '').strip()
    
    if not question:
        raise ValueError("Sample must contain a 'question' key")
    
    result = {'question': question}
    
    if is_cot:
        if 'cot' in sample:
            cot = sample.get('cot', '').strip()
            result['cot'] = cot
            if answer:
                result['answer'] = answer
                result['text'] = f"Question: {question}\n\nChain of Thought: {cot}\n\nAnswer: {answer}"
            else:
                result['text'] = f"Question: {question}\n\nChain of Thought: {cot}"
        else:
            if answer:
                result['answer'] = answer
                result['text'] = f"Question: {question}\n\nAnswer: {answer}"
            else:
                result['text'] = f"Question: {question}"
    else:
        if answer:
            result['answer'] = answer
            result['text'] = f"Question: {question}\n\nAnswer: {answer}"
        else:
            result['text'] = f"Question: {question}"
    
    return result
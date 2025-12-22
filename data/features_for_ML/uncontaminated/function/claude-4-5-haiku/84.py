import anthropic
from typing import List, Dict


def evaluate_dicts(pred: List[Dict], gold: List[Dict]):
    """
    Evaluate predicted dictionaries against gold standard dictionaries using Claude.
    
    Args:
        pred: List of predicted dictionaries
        gold: List of gold standard dictionaries
    
    Returns:
        Evaluation results from Claude
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Please evaluate the following predicted dictionaries against the gold standard dictionaries.

Predicted dictionaries:
{pred}

Gold standard dictionaries:
{gold}

Provide a detailed evaluation including:
1. Accuracy metrics (how many predictions match the gold standard)
2. Key differences between predictions and gold standard
3. Overall assessment of prediction quality
4. Specific areas of strength and weakness"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    pred = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "Los Angeles"},
        {"name": "Bob", "age": 35, "city": "Chicago"}
    ]
    
    gold = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 26, "city": "Los Angeles"},
        {"name": "Bob", "age": 35, "city": "Chicago"}
    ]
    
    result = evaluate_dicts(pred, gold)
    print(result)
import anthropic
import json


def evaluate(pred, target, metrics, id2type):
    """
    Evaluate predictions against targets using Claude as a judge.
    
    Args:
        pred: Predicted output
        target: Target/ground truth output
        metrics: List of metrics to evaluate
        id2type: Dictionary mapping IDs to types
    
    Returns:
        Dictionary containing evaluation results for each metric
    """
    client = anthropic.Anthropic()
    
    # Prepare the evaluation prompt
    evaluation_prompt = f"""You are an expert evaluator. Please evaluate the following prediction against the target using the specified metrics.

Prediction: {pred}
Target: {target}
Metrics to evaluate: {', '.join(metrics)}
ID to Type mapping: {json.dumps(id2type)}

For each metric, provide a score between 0 and 1, and a brief explanation.
Return the results as a JSON object with metric names as keys and objects containing 'score' and 'explanation' as values.
Example format:
{{
    "metric_name": {{"score": 0.85, "explanation": "explanation here"}},
    "another_metric": {{"score": 0.92, "explanation": "explanation here"}}
}}"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": evaluation_prompt}
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text
    
    # Extract JSON from the response
    try:
        # Try to find JSON in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            results = json.loads(json_str)
        else:
            results = {"error": "Could not parse evaluation results"}
    except json.JSONDecodeError:
        results = {"error": "Invalid JSON in response", "raw_response": response_text}
    
    return results


if __name__ == "__main__":
    # Example usage
    pred = "The quick brown fox jumps over the lazy dog"
    target = "A fast brown fox jumps over a lazy dog"
    metrics = ["semantic_similarity", "word_overlap", "grammatical_correctness"]
    id2type = {"1": "noun", "2": "verb", "3": "adjective"}
    
    result = evaluate(pred, target, metrics, id2type)
    print(json.dumps(result, indent=2))
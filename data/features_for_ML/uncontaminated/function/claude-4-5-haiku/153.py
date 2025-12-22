import anthropic
import json
import re


def compute_score(solution_str, ground_truth) -> float:
    """
    Compute a score for a solution string against ground truth using Claude.
    
    Args:
        solution_str: The solution string to evaluate
        ground_truth: The ground truth to compare against
        
    Returns:
        A float score between 0 and 1 representing how well the solution matches ground truth
    """
    client = anthropic.Anthropic()
    
    prompt = f"""You are an expert evaluator. Compare the following solution against the ground truth and provide a score.

Solution:
{solution_str}

Ground Truth:
{ground_truth}

Evaluate how well the solution matches the ground truth. Consider:
1. Correctness of the answer
2. Completeness of the solution
3. Accuracy of any calculations or logic
4. Clarity and proper formatting

Provide your evaluation in the following JSON format:
{{
    "score": <float between 0 and 1>,
    "reasoning": "<brief explanation of the score>"
}}

Return ONLY the JSON object, no additional text."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
    json_match = re.search(r'\{[^{}]*"score"[^{}]*\}', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        result = json.loads(json_str)
        score = float(result.get("score", 0.0))
        return max(0.0, min(1.0, score))
    
    return 0.0
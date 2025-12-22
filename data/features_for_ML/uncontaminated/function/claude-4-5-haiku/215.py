import anthropic
import json
from dataclasses import dataclass


@dataclass
class CompareArgs:
    """Arguments for comparison"""
    name: str
    results: dict


def _compare_results_report(eval_set: str, left_side: CompareArgs, right_side: CompareArgs, output_format: str):
    """
    Compare two sets of results using Claude API with streaming.
    
    Args:
        eval_set: The evaluation set name
        left_side: Left side comparison arguments with name and results
        right_side: Right side comparison arguments with name and results
        output_format: Format for the output (e.g., 'json', 'markdown')
    
    Returns:
        A string containing the comparison report
    """
    client = anthropic.Anthropic()
    
    # Prepare the comparison prompt
    comparison_prompt = f"""Please compare the following two sets of results from the {eval_set} evaluation set.

Left side ({left_side.name}):
{json.dumps(left_side.results, indent=2)}

Right side ({right_side.name}):
{json.dumps(right_side.results, indent=2)}

Please provide a detailed comparison analysis highlighting:
1. Key differences between the two results
2. Performance metrics comparison
3. Strengths and weaknesses of each approach
4. Overall assessment

Format the output as {output_format}."""

    # Use streaming to get the response
    report_content = ""
    
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": comparison_prompt
            }
        ]
    ) as stream:
        for text in stream.text_stream:
            report_content += text
    
    return report_content


if __name__ == "__main__":
    # Example usage
    left_results = {
        "accuracy": 0.92,
        "precision": 0.89,
        "recall": 0.91,
        "f1_score": 0.90
    }
    
    right_results = {
        "accuracy": 0.88,
        "precision": 0.85,
        "recall": 0.87,
        "f1_score": 0.86
    }
    
    left = CompareArgs(name="Model A", results=left_results)
    right = CompareArgs(name="Model B", results=right_results)
    
    report = _compare_results_report(
        eval_set="Classification Task",
        left_side=left,
        right_side=right,
        output_format="markdown"
    )
    
    print(report)
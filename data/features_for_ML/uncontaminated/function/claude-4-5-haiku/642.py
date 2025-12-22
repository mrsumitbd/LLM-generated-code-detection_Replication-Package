import json
import re
from typing import Any, Dict
from anthropic import Anthropic

def extract_semantic_patterns(text: str) -> Dict[str, Any]:
    """
    Main entry point for extracting semantic patterns from code.
    Returns structured pattern data suitable for Qdrant metadata.
    """
    client = Anthropic()
    conversation_history = []
    
    # First turn: Initial analysis
    initial_prompt = f"""Analyze the following code and identify its semantic patterns. 
    Look for:
    1. Design patterns (e.g., singleton, factory, observer)
    2. Code structure patterns (e.g., MVC, layered architecture)
    3. Functional patterns (e.g., map-reduce, pipeline)
    4. Data flow patterns
    5. Error handling patterns
    
    Code to analyze:
    ```
    {text}
    ```
    
    Provide a structured analysis with identified patterns."""
    
    conversation_history.append({
        "role": "user",
        "content": initial_prompt
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=conversation_history
    )
    
    initial_analysis = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": initial_analysis
    })
    
    # Second turn: Extract specific metrics
    metrics_prompt = """Based on your analysis, provide specific metrics for these patterns:
    1. Pattern complexity (low/medium/high)
    2. Pattern frequency (how many times each pattern appears)
    3. Pattern relationships (how patterns interact)
    4. Code quality indicators based on patterns
    
    Format your response as a JSON object with these metrics."""
    
    conversation_history.append({
        "role": "user",
        "content": metrics_prompt
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=conversation_history
    )
    
    metrics_analysis = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": metrics_analysis
    })
    
    # Third turn: Generate recommendations
    recommendations_prompt = """Based on the patterns identified and metrics calculated, provide:
    1. Recommendations for improving code based on patterns
    2. Potential refactoring opportunities
    3. Best practices that could be applied
    4. Risk areas based on pattern analysis
    
    Format as a JSON object with actionable recommendations."""
    
    conversation_history.append({
        "role": "user",
        "content": recommendations_prompt
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=conversation_history
    )
    
    recommendations = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": recommendations
    })
    
    # Fourth turn: Create final structured output
    final_prompt = """Now create a comprehensive JSON summary that includes:
    1. identified_patterns: list of patterns found
    2. pattern_metrics: metrics for each pattern
    3. code_quality_score: overall score (0-100)
    4. complexity_level: low/medium/high
    5. recommendations: list of recommendations
    6. risk_areas: potential issues
    7. best_practices: applicable best practices
    
    Return ONLY valid JSON, no other text."""
    
    conversation_history.append({
        "role": "user",
        "content": final_prompt
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=conversation_history
    )
    
    final_response = response.content[0].text
    
    # Parse the JSON response
    json_match = re.search(r'\{[\s\S]*\}', final_response)
    if json_match:
        try:
            result = json.loads(json_match.group())
        except json.JSONDecodeError:
            result = {
                "identified_patterns": [],
                "pattern_metrics": {},
                "code_quality_score": 0,
                "complexity_level": "unknown",
                "recommendations": [],
                "risk_areas": [],
                "best_practices": []
            }
    else:
        result = {
            "identified_patterns": [],
            "pattern_metrics": {},
            "code_quality_score": 0,
            "complexity_level": "unknown",
            "recommendations": [],
            "risk_areas": [],
            "best_practices": []
        }
    
    # Ensure all required fields exist
    required_fields = {
        "identified_patterns": [],
        "pattern_metrics": {},
        "code_quality_score": 0,
        "complexity_level": "unknown",
        "recommendations": [],
        "risk_areas": [],
        "best_practices": [],
        "conversation_turns": len(conversation_history) // 2
    }
    
    for field, default_value in required_fields.items():
        if field not in result:
            result[field] = default_value
    
    return result


if __name__ == "__main__":
    # Example usage
    sample_code = """
    class DataProcessor:
        def __init__(self):
            self.data = []
        
        def process(self, items):
            return [self._transform(item) for item in items]
        
        def _transform(self, item):
            return item * 2
        
        def save(self, filename):
            with open(filename, 'w') as f:
                f.write(str(self.data))
    """
    
    patterns = extract_semantic_patterns(sample_code)
    print(json.dumps(patterns, indent=2))
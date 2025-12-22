import anthropic


def run_min_window(solution_class: type, s: str, t: str):
    """
    Run the minWindow method using Claude to generate the implementation.
    
    Args:
        solution_class: A class with a minWindow method to be implemented
        s: The string to search in
        t: The string containing characters to find
    
    Returns:
        The minimum window substring
    """
    client = anthropic.Anthropic()
    
    # Create a prompt for Claude to implement the minWindow function
    prompt = f"""You are an expert Python programmer. Implement the minWindow method for the Solution class.

The minWindow method should find the minimum window substring of s which will contain all the characters in t.

Method signature:
def minWindow(self, s: str, t: str) -> str:

Requirements:
- Find the minimum window substring of s that contains all characters from t
- If no such window exists, return an empty string
- The characters in t can be in any order in the window
- If there are duplicate characters in t, the window must contain at least that many of each character

Example:
- s = "ADOBECODEBANC", t = "ABC" -> "BANC"
- s = "a", t = "a" -> "a"
- s = "a", t = "aa" -> ""

Provide only the implementation of the minWindow method, nothing else. The method should be properly indented as a class method."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the implementation from Claude's response
    implementation = message.content[0].text
    
    # Clean up the implementation - remove markdown code blocks if present
    if implementation.startswith("```"):
        implementation = implementation.split("```")[1]
        if implementation.startswith("python"):
            implementation = implementation[6:]
    if implementation.endswith("```"):
        implementation = implementation[:-3]
    
    implementation = implementation.strip()
    
    # Create a namespace with the implementation
    namespace = {}
    exec(implementation, namespace)
    
    # Get the minWindow function from the namespace
    min_window_func = namespace.get('minWindow')
    
    if min_window_func is None:
        raise ValueError("Could not extract minWindow function from Claude's response")
    
    # Add the method to the solution class
    solution_class.minWindow = min_window_func
    
    # Create an instance and call the method
    solution = solution_class()
    result = solution.minWindow(s, t)
    
    return result


class Solution:
    pass


if __name__ == "__main__":
    # Test the implementation
    test_cases = [
        ("ADOBECODEBANC", "ABC"),
        ("a", "a"),
        ("a", "aa"),
        ("ab", "b"),
        ("abc", "cba"),
    ]
    
    for s, t in test_cases:
        result = run_min_window(Solution, s, t)
        print(f"s = '{s}', t = '{t}' -> '{result}'")
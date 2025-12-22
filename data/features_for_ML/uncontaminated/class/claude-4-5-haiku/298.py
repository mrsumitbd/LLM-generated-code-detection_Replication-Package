import anthropic
import json
import asyncio
from typing import Any

class ToolFuzzer:
    """Orchestrates fuzzing of MCP tools."""

    def __init__(self, max_concurrency: int = 5):
        self.max_concurrency = max_concurrency
        self.client = anthropic.Anthropic()
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def fuzz_tool(self, tool_name: str, tool_description: str, tool_input_schema: dict) -> dict:
        """Fuzz a single tool by generating test inputs and calling it."""
        async with self.semaphore:
            # Generate fuzzing test cases using Claude
            prompt = f"""Generate 5 diverse test cases for fuzzing the following tool:

Tool Name: {tool_name}
Description: {tool_description}
Input Schema: {json.dumps(tool_input_schema, indent=2)}

For each test case, provide:
1. A description of what the test case is testing
2. The input parameters as a JSON object
3. Expected behavior or potential issues

Format your response as a JSON array of objects with keys: "description", "input", "expected_behavior"
"""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse the response
            response_text = message.content[0].text
            
            # Extract JSON from the response
            try:
                # Try to find JSON array in the response
                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    test_cases = json.loads(json_str)
                else:
                    test_cases = []
            except json.JSONDecodeError:
                test_cases = []

            return {
                "tool_name": tool_name,
                "test_cases": test_cases,
                "raw_response": response_text
            }

    async def fuzz_tools(self, tools: list[dict]) -> list[dict]:
        """Fuzz multiple tools concurrently."""
        tasks = []
        for tool in tools:
            task = self.fuzz_tool(
                tool_name=tool.get("name", "unknown"),
                tool_description=tool.get("description", ""),
                tool_input_schema=tool.get("input_schema", {})
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results

    def run_fuzzing(self, tools: list[dict]) -> list[dict]:
        """Run fuzzing on tools (synchronous wrapper)."""
        return asyncio.run(self.fuzz_tools(tools))


# Example usage and testing
if __name__ == "__main__":
    # Create a fuzzer instance
    fuzzer = ToolFuzzer(max_concurrency=3)

    # Define some sample tools to fuzz
    sample_tools = [
        {
            "name": "calculator",
            "description": "Performs basic arithmetic operations",
            "input_schema": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        },
        {
            "name": "text_processor",
            "description": "Processes and transforms text",
            "input_schema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "operation": {"type": "string", "enum": ["uppercase", "lowercase", "reverse", "count_words"]},
                    "max_length": {"type": "integer", "minimum": 1}
                },
                "required": ["text", "operation"]
            }
        }
    ]

    # Run fuzzing
    results = fuzzer.run_fuzzing(sample_tools)

    # Display results
    for result in results:
        print(f"\n{'='*60}")
        print(f"Tool: {result['tool_name']}")
        print(f"{'='*60}")
        print(f"Generated {len(result['test_cases'])} test cases:")
        for i, test_case in enumerate(result['test_cases'], 1):
            print(f"\nTest Case {i}:")
            print(f"  Description: {test_case.get('description', 'N/A')}")
            print(f"  Input: {json.dumps(test_case.get('input', {}), indent=4)}")
            print(f"  Expected: {test_case.get('expected_behavior', 'N/A')}")
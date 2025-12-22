import anthropic
import json
import re


class MessageValidator:

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def validate_message(self, message: str, schema: dict) -> dict:
        """
        Validate a message against a schema using Claude.
        
        Args:
            message: The message to validate
            schema: The schema to validate against
            
        Returns:
            A dictionary with validation results
        """
        prompt = f"""You are a message validator. Validate the following message against the provided schema.

Message to validate:
{message}

Schema:
{json.dumps(schema, indent=2)}

Respond with a JSON object containing:
- "valid": boolean indicating if the message is valid
- "errors": list of validation errors (empty if valid)
- "warnings": list of warnings (empty if none)
- "details": any additional details about the validation

Respond ONLY with the JSON object, no other text."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = response.content[0].text
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response_text)
        
        return result

    def validate_batch(self, messages: list, schema: dict) -> list:
        """
        Validate multiple messages against a schema.
        
        Args:
            messages: List of messages to validate
            schema: The schema to validate against
            
        Returns:
            List of validation results
        """
        results = []
        for message in messages:
            result = self.validate_message(message, schema)
            results.append(result)
        return results

    def get_validation_report(self, messages: list, schema: dict) -> dict:
        """
        Get a comprehensive validation report for multiple messages.
        
        Args:
            messages: List of messages to validate
            schema: The schema to validate against
            
        Returns:
            A dictionary with overall validation statistics
        """
        results = self.validate_batch(messages, schema)
        
        valid_count = sum(1 for r in results if r.get("valid", False))
        total_count = len(results)
        
        all_errors = []
        all_warnings = []
        
        for result in results:
            all_errors.extend(result.get("errors", []))
            all_warnings.extend(result.get("warnings", []))
        
        return {
            "total_messages": total_count,
            "valid_messages": valid_count,
            "invalid_messages": total_count - valid_count,
            "success_rate": valid_count / total_count if total_count > 0 else 0,
            "total_errors": len(all_errors),
            "total_warnings": len(all_warnings),
            "all_errors": all_errors,
            "all_warnings": all_warnings,
            "detailed_results": results
        }
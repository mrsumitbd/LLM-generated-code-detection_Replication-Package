import anthropic
from google.protobuf import any_pb2
from google.protobuf.json_format import MessageToDict
import json


class CommandGetDbSchemas:

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def Unpack(self, any_message):
        """
        Unpacks an Any message and processes it using Claude to extract database schemas.
        
        Args:
            any_message: A protobuf Any message containing serialized data
            
        Returns:
            A dictionary containing the unpacked message and Claude's analysis
        """
        # Unpack the Any message
        unpacked_message = any_pb2.Any()
        if isinstance(any_message, bytes):
            unpacked_message.ParseFromString(any_message)
        else:
            unpacked_message = any_message
        
        # Convert the unpacked message to a dictionary for easier handling
        message_dict = MessageToDict(unpacked_message)
        
        # Prepare the prompt for Claude
        prompt = f"""You are a database schema expert. I have received a protobuf Any message that may contain database schema information.

Here is the unpacked message data:
{json.dumps(message_dict, indent=2)}

Please analyze this message and:
1. Identify if it contains database schema information
2. Extract any table names, column definitions, data types, and constraints
3. Provide a structured summary of the database schemas found
4. If no schema information is found, explain what the message appears to contain

Format your response as a JSON object with the following structure:
{{
    "contains_schema": boolean,
    "schemas": [
        {{
            "table_name": "string",
            "columns": [
                {{
                    "name": "string",
                    "type": "string",
                    "constraints": ["string"]
                }}
            ]
        }}
    ],
    "summary": "string",
    "raw_data": object
}}"""
        
        # Call Claude API
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the response
        response_text = message.content[0].text
        
        # Try to parse the response as JSON
        try:
            # Find JSON content in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed_response = json.loads(json_str)
            else:
                parsed_response = {"summary": response_text}
        except json.JSONDecodeError:
            parsed_response = {"summary": response_text}
        
        # Return the result
        return {
            "unpacked_message": message_dict,
            "analysis": parsed_response,
            "raw_response": response_text
        }
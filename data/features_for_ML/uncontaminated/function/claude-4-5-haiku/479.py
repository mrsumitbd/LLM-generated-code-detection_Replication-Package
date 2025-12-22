import anthropic
import re


def add_cdata_to_function_body(xml_string):
    """
    Uses Claude to add CDATA sections to function bodies in XML.
    
    Args:
        xml_string: XML string containing function definitions
        
    Returns:
        Modified XML string with CDATA sections added to function bodies
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Please modify the following XML by adding CDATA sections around the content inside <function_body> tags. 
                
The CDATA section should wrap the entire content of each function_body element.

Here's the XML to modify:

{xml_string}

Please return only the modified XML without any explanation."""
            }
        ]
    )
    
    result = message.content[0].text
    
    # Clean up the result if it has markdown code blocks
    if result.startswith("```xml"):
        result = result[6:]
    if result.startswith("```"):
        result = result[3:]
    if result.endswith("```"):
        result = result[:-3]
    
    return result.strip()


if __name__ == "__main__":
    # Test with sample XML
    sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
<functions>
    <function>
        <name>calculate</name>
        <function_body>
            def calculate(a, b):
                return a + b
        </function_body>
    </function>
    <function>
        <name>greet</name>
        <function_body>
            def greet(name):
                print(f"Hello, {name}!")
        </function_body>
    </function>
</functions>"""
    
    result = add_cdata_to_function_body(sample_xml)
    print("Modified XML:")
    print(result)
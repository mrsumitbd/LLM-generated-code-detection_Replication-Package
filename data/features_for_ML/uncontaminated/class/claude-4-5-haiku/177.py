import anthropic
import json
from functools import wraps


class DataParserFactory:
    _loaders = {}

    @classmethod
    def register_loader(cls, format_name: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            cls._loaders[format_name] = wrapper
            return wrapper
        return decorator

    @classmethod
    def get_loader(cls, format_name: str, **kwargs) -> object:
        if format_name not in cls._loaders:
            raise ValueError(f"No loader registered for format: {format_name}")
        
        loader_func = cls._loaders[format_name]
        
        def parse_with_claude(data: str) -> dict:
            client = anthropic.Anthropic()
            
            prompt = f"""Parse the following {format_name} data and return it as a JSON object.
            
Data to parse:
{data}

Please parse this data and return a valid JSON object with the parsed content."""
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                pass
            
            return {"raw_response": response_text}
        
        return parse_with_claude


@DataParserFactory.register_loader("csv")
def parse_csv(data: str) -> dict:
    lines = data.strip().split('\n')
    if not lines:
        return {"error": "Empty data"}
    
    headers = lines[0].split(',')
    rows = []
    for line in lines[1:]:
        values = line.split(',')
        row = {headers[i]: values[i] if i < len(values) else "" for i in range(len(headers))}
        rows.append(row)
    
    return {"headers": headers, "rows": rows}


@DataParserFactory.register_loader("json")
def parse_json(data: str) -> dict:
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}


@DataParserFactory.register_loader("xml")
def parse_xml(data: str) -> dict:
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(data)
        
        def element_to_dict(elem):
            result = {"tag": elem.tag, "attributes": elem.attrib}
            if elem.text and elem.text.strip():
                result["text"] = elem.text.strip()
            children = []
            for child in elem:
                children.append(element_to_dict(child))
            if children:
                result["children"] = children
            return result
        
        return element_to_dict(root)
    except Exception as e:
        return {"error": f"Invalid XML: {str(e)}"}


if __name__ == "__main__":
    csv_parser = DataParserFactory.get_loader("csv")
    csv_data = """name,age,city
John,30,New York
Jane,25,Los Angeles"""
    print("CSV Parser Result:")
    print(csv_parser(csv_data))
    
    json_parser = DataParserFactory.get_loader("json")
    json_data = '{"name": "John", "age": 30, "city": "New York"}'
    print("\nJSON Parser Result:")
    print(json_parser(json_data))
    
    xml_parser = DataParserFactory.get_loader("xml")
    xml_data = '<person><name>John</name><age>30</age></person>'
    print("\nXML Parser Result:")
    print(xml_parser(xml_data))
    
    claude_parser = DataParserFactory.get_loader("custom_format")
    custom_data = "Name: John, Age: 30, City: New York"
    print("\nClaude Parser Result:")
    print(claude_parser(custom_data))
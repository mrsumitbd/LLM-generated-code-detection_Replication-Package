import re

def add_cdata_to_function_body(xml_string):
    pattern = r'<function_body>(.*?)</function_body>'
    match = re.search(pattern, xml_string, re.DOTALL)
    if match:
        function_body = match.group(1)
        cdata_body = f'<![CDATA[{function_body}]]>'
        return xml_string.replace(match.group(), cdata_body)
    return xml_string
def add_cdata_to_function_body(xml_string):
    import re
    pattern = r'<function>(.*?)</function>'
    xml_string = re.sub(pattern, r'<function><![CDATA[\1]]></function>', xml_string)
    return xml_string
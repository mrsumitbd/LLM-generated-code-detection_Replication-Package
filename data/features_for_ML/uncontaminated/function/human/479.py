import re

def add_cdata_to_function_body(xml_string):
        pattern = r"(<function_body>)(.*?)(</function_body>)"
        replacement = r"\1<![CDATA[\2]]>\3"
        updated_xml_string = re.sub(pattern, replacement, xml_string, flags=re.DOTALL)
        return updated_xml_string
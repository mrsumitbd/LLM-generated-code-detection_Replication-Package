import re

def add_cdata_to_function_body(xml_string):
    """
    Wrap the content of every <body> element in the given XML string with a CDATA section.
    The function assumes that the body content does not contain the CDATA end marker ']]>'.

    Parameters
    ----------
    xml_string : str
        The XML document as a string.

    Returns
    -------
    str
        The XML document with CDATA sections added around each <body> element's content.
    """
    # Pattern to capture the content inside <body> tags, including newlines.
    pattern = re.compile(r'(<body\s*[^>]*>)(.*?)(</body>)', re.DOTALL)

    def repl(match):
        start_tag, body_content, end_tag = match.groups()
        # Escape any existing CDATA end markers inside the body content
        # (though this is unlikely in typical use cases).
        safe_content = body_content.replace(']]>', ']]]]><![CDATA[>')
        return f"{start_tag}<![CDATA[{safe_content}]]>{end_tag}"

    return pattern.sub(repl, xml_string)
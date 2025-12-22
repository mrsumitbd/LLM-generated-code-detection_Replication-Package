import re

def _strip_properly_formatted_commas(expr: str) -> str:
    """
    Remove commas that are used as thousands separators in numeric literals
    while preserving commas that are part of tuple/list/dict syntax or
    string literals.

    Parameters
    ----------
    expr : str
        The expression string to process.

    Returns
    -------
    str
        The expression with numeric commas removed.
    """
    # Find all string literal spans (single, double, triple quotes)
    string_pattern = r'(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\"|\'(?:\\.|[^\\\'])*\'|\"(?:\\.|[^\\\"])*\")'
    string_spans = [m.span() for m in re.finditer(string_pattern, expr)]

    # Mark characters that are inside string literals
    inside_string = [False] * len(expr)
    for start, end in string_spans:
        for i in range(start, end):
            inside_string[i] = True

    # Pattern to match numbers with commas (including optional sign and exponent)
    num_pattern = (
        r'(?<![A-Za-z0-9_])'          # not preceded by a word character
        r'[-+]?'                      # optional sign
        r'\d{1,3}(?:,\d{3})+'         # digits with commas
        r'(?:\.\d+)?'                 # optional fractional part
        r'(?:[eE][+-]?\d+)?'          # optional exponent
        r'(?![A-Za-z0-9_])'           # not followed by a word character
    )

    # Build the result by replacing matched numbers outside string literals
    result_parts = []
    last = 0
    for m in re.finditer(num_pattern, expr):
        start, end = m.span()
        # Skip if the match overlaps a string literal
        if any(inside_string[i] for i in range(start, end)):
            continue
        result_parts.append(expr[last:start])
        num_no_commas = m.group().replace(',', '')
        result_parts.append(num_no_commas)
        last = end
    result_parts.append(expr[last:])

    return ''.join(result_parts)
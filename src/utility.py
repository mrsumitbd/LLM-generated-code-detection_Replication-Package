from os import listdir
from os.path import isfile, join
import re, ast
from typing import List, Optional


def list_files(folder_path, all_files=True, extension=None):
    if all_files:
        return [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    else:
        if extension is None:
            raise ValueError("Extension cannot be None if only a fixed type of files are to be listed.")
        else:
            return [f for f in listdir(folder_path) if (isfile(join(folder_path, f)) and f.endswith(f".{extension}"))]


def remove_comments(code_text):
    """
    Remove comments from Python code while preserving strings and docstrings.
    Uses AST for proper parsing.
    """
    try:
        # Parse the code
        tree = ast.parse(code_text)
        lines = code_text.split('\n')

        # Track which lines have docstrings (to preserve them)
        docstring_lines = set()

        for node in ast.walk(tree):
            # Find all docstrings
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node, clean=False)
                if docstring and hasattr(node, 'body') and len(node.body) > 0:
                    first_stmt = node.body[0]
                    if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Constant):
                        # Mark docstring lines as protected
                        for line_num in range(first_stmt.lineno - 1, first_stmt.end_lineno):
                            docstring_lines.add(line_num)

        # Remove single-line comments
        cleaned_lines = []
        for i, line in enumerate(lines):
            if i in docstring_lines:
                # Preserve docstring lines completely
                cleaned_lines.append(line)
            else:
                # Remove comments, but be careful about strings
                cleaned_line = remove_comment_from_line(line)
                cleaned_lines.append(cleaned_line)

        return '\n'.join(cleaned_lines)

    except SyntaxError:
        # If parsing fails, return original
        return code_text


def remove_comment_from_line(line):
    """
    Remove # comments from a line, preserving # inside strings.
    """
    in_string = False
    string_char = None
    escaped = False

    for i, char in enumerate(line):
        if escaped:
            escaped = False
            continue

        if char == '\\':
            escaped = True
            continue

        # Track string boundaries
        if char in ('"', "'") and not in_string:
            in_string = True
            string_char = char
        elif char == string_char and in_string:
            in_string = False
            string_char = None

        # Found comment outside string
        elif char == '#' and not in_string:
            return line[:i].rstrip()  # Remove everything after #

    return line


def remove_all_comments_and_docstrings(code_text):
    """
    Remove ALL comments including docstrings.
    Use AST to remove function/class docstrings.
    """
    try:
        tree = ast.parse(code_text)

        # Remove docstrings from functions and classes
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if (node.body and
                        isinstance(node.body[0], ast.Expr) and
                        isinstance(node.body[0].value, ast.Constant)):
                    # Remove the docstring
                    node.body = node.body[1:] if len(node.body) > 1 else [ast.Pass()]

        # Reconstruct code
        code_without_docstrings = ast.unparse(tree)

        # Now remove single-line comments
        return remove_comments(code_without_docstrings)

    except SyntaxError:
        return code_text


def remove_main(code):
    pattern = r'if\s+__name__\s*==\s*["\']__main__["\']\s*:\s*(?:\n[ \t]+.+)+'

    try:
        code = re.sub(pattern, '', code, flags=re.MULTILINE)

        # Clean up extra blank lines that might be left
        code = re.sub(r'\n\n\n+', '\n\n', code)

        return code.strip()
    except:
        return None


def check_for_empty_body(code_body):
    if code_body == "":
        return True
    # empty = re.search(r"def\s\S+\([\s\S]*?\):\s+.*\s+pass|def\s\S+\([\s\S]*?\).*:\s+$", code_body, re.MULTILINE)
    code_left = re.sub(r"(import\s.*\n+)*def\s[\d\S]+\s*\(.*?\).*?:|(from\s.*\n+)*def\s[\d\S]+\s*\(.*?\).*?:", "",
                       code_body, re.MULTILINE)

    # if there is a main function remove it
    code_left = remove_main(code_left)

    if len(code_left.split()) == 0:
        return True
    elif len(code_left.split()) == 1 and code_left.split()[0] == "pass":
        return True
    else:
        return False

def extract_code_from_response(response: str) -> Optional[str]:
    """
    Extract Python code from LLM response, removing natural language explanations.

    Args:
        response: The full response from the LLM

    Returns:
        Extracted Python code string, or None if no valid code found
    """
    if response is None:
        return None

    # Strategy 1: Extract code from markdown code blocks
    # Matches ```python or ``` followed by code
    markdown_pattern = r'```(?:python)?\s*\n(.*?)\n```'
    markdown_matches = re.findall(markdown_pattern, response, re.DOTALL)

    if markdown_matches:
        # Return the first (usually only) code block
        code = markdown_matches[0].strip()
        return code if code else None

    # Strategy 2: No markdown blocks - try to identify where code starts
    lines = response.split('\n')
    code_lines = []
    in_code = False

    for line in lines:
        stripped = line.strip()

        # Skip common natural language patterns at the start
        if not in_code:
            # Skip lines that are clearly natural language
            skip_patterns = [
                r'^here is',
                r'^here\'s',
                r'^i have',
                r'^i\'ve',
                r'^this is',
                r'^below is',
                r'^the complete',
                r'^the implementation',
                r'^certainly',
                r'^sure',
            ]
            if any(re.match(pattern, stripped, re.IGNORECASE) for pattern in skip_patterns):
                continue

            # Start collecting when we see Python code indicators
            if stripped.startswith(('class ', 'def ', 'import ', 'from ', '@')):
                in_code = True
                code_lines.append(line)
            # Also start if we see common Python keywords
            elif stripped.startswith(('if ', 'for ', 'while ', 'try:', 'with ')):
                in_code = True
                code_lines.append(line)
        else:
            # Once in code, keep collecting until we hit natural language again
            # Stop if we hit explanatory text (lines that start with letters but aren't code)
            if stripped and not stripped.startswith('#'):
                # Check if line looks like natural language (no special Python chars)
                if re.match(r'^[A-Z][a-z].*(:|\.)\s*$', stripped):
                    # Looks like a sentence, stop collecting
                    break
            code_lines.append(line)

    if code_lines:
        code = '\n'.join(code_lines).strip()
        return code if code else None

    # Strategy 3: If still no code found, return the whole response
    # (assuming it's all code with no explanations)
    return response.strip() if response.strip() else None

def extract_code_from_responses(responses: List[str]) -> List[Optional[str]]:
    """
    Extract code from a list of LLM responses.

    Args:
        responses: List of LLM responses

    Returns:
        List of extracted code snippets (None for failed extractions)
    """
    return [extract_code_from_response(response) for response in responses]

def validate_python_syntax(code: str) -> bool:
    """
    Validate that extracted code is valid Python syntax.

    Args:
        code: Python code string

    Returns:
        True if valid Python syntax, False otherwise
    """
    if not code:
        return False

    try:
        import ast
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def post_process_batch_results(
        code_snippets: List[Optional[str]],
        validate_syntax: bool = True
) -> List[Optional[str]]:
    """
    Post-process batch generation results to extract clean code.

    Args:
        code_snippets: Raw outputs from batch_generate_with_claude
        validate_syntax: If True, validate Python syntax and set invalid to None

    Returns:
        List of cleaned code snippets
    """
    # Extract code from responses
    cleaned_snippets = extract_code_from_responses(code_snippets)

    # Optionally validate syntax
    if validate_syntax:
        for i, snippet in enumerate(cleaned_snippets):
            if snippet and not validate_python_syntax(snippet):
                print(f"Warning: Snippet {i} has invalid syntax, setting to None")
                cleaned_snippets[i] = None

    return cleaned_snippets
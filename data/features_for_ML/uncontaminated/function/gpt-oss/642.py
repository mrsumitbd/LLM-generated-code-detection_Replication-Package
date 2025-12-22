from typing import Dict, Any, List
import re

def extract_semantic_patterns(text: str) -> Dict[str, Any]:
    """
    Main entry point for extracting semantic patterns from code.
    Returns structured pattern data suitable for Qdrant metadata.
    """
    # Helper regex patterns
    import_re = re.compile(r'^\s*(import\s+[\w\.]+|from\s+[\w\.]+\s+import\s+[\w\*,\s]+)', re.MULTILINE)
    func_re = re.compile(r'^\s*def\s+(\w+)\s*\(([^)]*)\)\s*:', re.MULTILINE)
    async_func_re = re.compile(r'^\s*async\s+def\s+(\w+)\s*\(([^)]*)\)\s*:', re.MULTILINE)
    class_re = re.compile(r'^\s*class\s+(\w+)\s*(\([^)]*\))?:', re.MULTILINE)
    lambda_re = re.compile(r'(\w+)\s*=\s*lambda\s+([^:]+):', re.MULTILINE)
    comment_re = re.compile(r'^\s*#(.*)', re.MULTILINE)
    docstring_re = re.compile(r'(""".*?"""|\'\'\'.*?\'\'\')', re.DOTALL)

    # Extract imports
    imports: List[str] = [m.group(0).strip() for m in import_re.finditer(text)]

    # Extract functions
    functions: List[Dict[str, Any]] = []
    for m in func_re.finditer(text):
        name, params = m.group(1), m.group(2)
        functions.append({"name": name, "params": [p.strip() for p in params.split(",") if p.strip()]})
    for m in async_func_re.finditer(text):
        name, params = m.group(1), m.group(2)
        functions.append({"name": name, "params": [p.strip() for p in params.split(",") if p.strip()], "async": True})

    # Extract classes
    classes: List[Dict[str, Any]] = []
    for m in class_re.finditer(text):
        name, bases = m.group(1), m.group(2)
        base_list = []
        if bases:
            base_list = [b.strip() for b in bases.strip("()").split(",") if b.strip()]
        classes.append({"name": name, "bases": base_list})

    # Extract lambdas
    lambdas: List[Dict[str, Any]] = []
    for m in lambda_re.finditer(text):
        var, params = m.group(1), m.group(2)
        lambdas.append({"var": var, "params": [p.strip() for p in params.split(",") if p.strip()]})

    # Extract comments
    comments: List[str] = [m.group(1).strip() for m in comment_re.finditer(text)]

    # Extract docstrings
    docstrings: List[str] = [m.group(0).strip() for m in docstring_re.finditer(text)]

    return {
        "imports": imports,
        "functions": functions,
        "classes": classes,
        "lambdas": lambdas,
        "comments": comments,
        "docstrings": docstrings,
    }
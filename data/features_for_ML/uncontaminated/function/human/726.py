import re, textwrap
from itertools import dropwhile, takewhile

def _parse_from_test_patch(test_patch: str, func_name: str) -> str:
        patch_lines = test_patch.splitlines()
        start_iter = dropwhile(
            lambda l: not re.search(rf'\bdef\s+{re.escape(func_name)}\b', l), patch_lines
        )
        snippet = list(
            takewhile(lambda l: not l.startswith('diff --git'), start_iter)
        )
        if snippet:
            return "\n".join(l for l in snippet)
        else:
            return ""
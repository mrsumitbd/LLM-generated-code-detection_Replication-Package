import re

def _extract_param_type(docstring, param_name):
        """
        Extracts the parameter type from the function's docstring.
        """
        if docstring:
            pattern = re.escape(param_name) + r"\s*\((.*?)\):"
            match = re.search(pattern, docstring)
            if match:
                return match.group(1).strip()
        return "Unknown"
import re
from typing import Optional

def _extract_param_type(docstring: Optional[str], param_name: str) -> Optional[str]:
    """
    Extracts the parameter type from the function's docstring.

    Supports common docstring styles:
    - Google style: ``param_name (type): description``
    - NumPy style: ``param_name : type`` or ``param_name: type``
    - reST style: ``:param param_name: description`` (type not extracted)

    Parameters
    ----------
    docstring : str | None
        The docstring to parse.
    param_name : str
        The name of the parameter to look for.

    Returns
    -------
    str | None
        The extracted type string, or ``None`` if no type could be found.
    """
    if not docstring:
        return None

    # Compile regex patterns once
    google_pat = re.compile(rf"^{re.escape(param_name)}\s*\(([^)]+)\)")
    numpy_pat = re.compile(rf"^{re.escape(param_name)}\s*:\s*([^\n]+)")
    rest_pat = re.compile(rf"^:param\s+{re.escape(param_name)}:\s*([^\n]+)")

    for raw_line in docstring.splitlines():
        line = raw_line.strip()

        # Google style: param_name (type)
        m = google_pat.match(line)
        if m:
            return m.group(1).strip()

        # NumPy style: param_name : type
        m = numpy_pat.match(line)
        if m:
            candidate = m.group(1).strip()
            # If the candidate looks like a description (contains '(' or ')')
            # skip it; otherwise treat it as a type.
            if '(' not in candidate and ')' not in candidate:
                return candidate

        # reST style: :param param_name: description
        # Type is usually not present in this line; skip.
        if rest_pat.match(line):
            continue

    return None
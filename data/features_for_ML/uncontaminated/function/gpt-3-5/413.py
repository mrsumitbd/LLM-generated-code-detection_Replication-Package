def fix_output_references(yaml_str: str) -> str:
    import re

    def replace_output(match):
        return f"{{{{ outputs.{match.group(1)} }}}}"

    return re.sub(r"\{\{ outputs\.([^}]+) \}\}", replace_output, yaml_str)
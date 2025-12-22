def make_code_text(files_dict, add_line_numbers=True):
    code_text = ""
    for filename, content in files_dict.items():
        code_text += f"# {filename}\n"
        if add_line_numbers:
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                code_text += f"{i:>5} {line}\n"
        else:
            code_text += f"{content}\n"
        code_text += "\n"
    return code_text.strip()
def make_code_text(files_dict, add_line_numbers=True):
    code_text = ''
    for file_name, lines in files_dict.items():
        code_text += f'{file_name}:\n'
        if add_line_numbers:
            for i, line in enumerate(lines, start=1):
                code_text += f'{i}: {line}\n'
        else:
            for line in lines:
                code_text += f'{line}\n'
        code_text += '\n'
    return code_text
def _format_vis_msg(msg: str):
    if not msg:
        return ""

    lines = msg.split("\n")
    formatted_lines = []

    for line in lines:
        if line.strip():
            formatted_lines.append(line.strip())

    return "\n".join(formatted_lines)
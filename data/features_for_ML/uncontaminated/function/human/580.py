def replace_context(match):
            key = match.group(1)
            if key in context:
                return str(context[key])
            return match.group(0)  # leave untouched
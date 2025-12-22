def get_argument_content(element, directive_name, argument_name):
    if hasattr(element, 'directives'):
        for directive in element.directives:
            if directive.name.value == directive_name:
                for argument in directive.arguments:
                    if argument.name.value == argument_name:
                        if argument.value:
                            return argument.value.value
    return None
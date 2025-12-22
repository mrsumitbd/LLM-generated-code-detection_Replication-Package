def validate_arguments(args):
    """
        new function for an easier validation of the args passed to the function, due the fact there are now 2 calls methods. If mail_body_html is passed, nor subject and to_address are mandatory
    """
    if 'mail_body_html' in args:
        if 'subject' not in args or 'to_address' not in args:
            raise ValueError("If 'mail_body_html' is passed, 'subject' and 'to_address' are mandatory.")
    return True
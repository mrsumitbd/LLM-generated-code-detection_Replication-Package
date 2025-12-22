def validate_arguments(args):
    if 'mail_body_html' in args:
        return True
    elif 'subject' in args and 'to_address' in args:
        return True
    else:
        return False
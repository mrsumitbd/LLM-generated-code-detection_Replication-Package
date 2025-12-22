def validate_arguments(args):
    """
        new function for an easier validation of the args passed to the function, due the fact there are now 2 calls methods. If mail_body_html is passed, nor subject and to_address are mandatory
    """
    required_fields = ['mail_body_html', 'subject', 'to_address']
    
    if 'mail_body_html' in args and args['mail_body_html']:
        return True
    
    for field in required_fields:
        if field not in args or not args[field]:
            return False
    
    return True
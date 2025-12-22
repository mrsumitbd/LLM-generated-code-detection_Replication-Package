def validate_arguments(args):
    """
    Validate the arguments passed to the mail sending function.

    The function accepts two calling styles:
        1. The legacy style where `subject` and `to_address` are mandatory.
        2. The new style where `mail_body_html` is provided; in this case
           `subject` and `to_address` are optional.

    Parameters
    ----------
    args : dict or argparse.Namespace
        The arguments to validate. Keys may include:
            - 'subject'
            - 'to_address'
            - 'mail_body_html'
            - any other keys are ignored.

    Raises
    ------
    ValueError
        If the required arguments are missing according to the rules above.
    """
    # Normalise args to a dictionary
    if isinstance(args, dict):
        arg_dict = args
    else:
        # Assume argparse.Namespace or similar
        arg_dict = vars(args)

    # Determine if the new style is being used
    mail_body_html = arg_dict.get("mail_body_html")
    new_style = mail_body_html is not None

    # In the legacy style, subject and to_address are mandatory
    if not new_style:
        missing = []
        if not arg_dict.get("subject"):
            missing.append("subject")
        if not arg_dict.get("to_address"):
            missing.append("to_address")
        if missing:
            raise ValueError(
                f"Missing mandatory argument(s) for legacy call: {', '.join(missing)}"
            )
    # In the new style, no further validation is required
    return True
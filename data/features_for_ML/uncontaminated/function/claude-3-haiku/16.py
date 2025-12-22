import re
from typing import List, Tuple

def search_emails_handler(args: dict, context: dict) -> Tuple[List[str], dict]:
    """
    Searches for email addresses in the provided text and returns a list of found emails.

    Args:
        args (dict): A dictionary containing the following keys:
            - 'text': The text to search for email addresses.
        context (dict): A dictionary containing additional context information.

    Returns:
        Tuple[List[str], dict]: A tuple containing a list of found email addresses and an updated context dictionary.
    """
    text = args.get('text', '')
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return emails, context
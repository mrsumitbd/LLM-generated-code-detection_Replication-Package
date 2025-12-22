def init_prompt():
    """
    Initializes the command-line prompt and returns the prompt string.

    Returns:
        str: The initialized prompt string.
    """
    import os
    import sys
    import getpass

    # Get the current username
    username = getpass.getuser()

    # Get the current working directory
    cwd = os.getcwd()

    # Construct the prompt string
    prompt = f"{username}@{os.path.basename(sys.argv[0])}:{cwd}$ "

    return prompt
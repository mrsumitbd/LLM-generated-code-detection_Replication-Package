def generate_password_hash_command():
    """Generates a bcrypt hash for a given password, for Web UI authentication.

    This interactive command securely prompts the user to enter a new password
    and then confirm it. Upon successful confirmation, it generates a bcrypt
    hash of the password using the application's configured `passlib.context.CryptContext`.

    The output is the generated hash, which is intended to be used as the value
    for the ``BSM_PASSWORD`` (or equivalent, based on
    :const:`~.config.const.env_name`) environment variable. This variable,
    along with ``BSM_USERNAME``, secures access to the web interface.

    The command provides clear instructions on how to use the generated hash.
    Input is hidden during password entry for security.
    """
    import getpass
    from . import config
    
    print("\n" + "="*60)
    print("Password Hash Generator for Web UI Authentication")
    print("="*60)
    print("\nThis tool will generate a bcrypt hash for your password.")
    print("The hash can be used as the BSM_PASSWORD environment variable.\n")
    
    while True:
        password = getpass.getpass("Enter new password: ")
        
        if not password:
            print("Error: Password cannot be empty. Please try again.\n")
            continue
        
        password_confirm = getpass.getpass("Confirm password: ")
        
        if password != password_confirm:
            print("Error: Passwords do not match. Please try again.\n")
            continue
        
        break
    
    # Generate the hash using the application's CryptContext
    password_hash = config.crypt_context.hash(password)
    
    print("\n" + "="*60)
    print("Generated Password Hash:")
    print("="*60)
    print(f"\n{password_hash}\n")
    print("="*60)
    print("Usage Instructions:")
    print("="*60)
    print(f"\nSet this hash as an environment variable:")
    print(f"  export {config.const.env_name}_PASSWORD='{password_hash}'")
    print(f"\nOr add it to your .env file:")
    print(f"  {config.const.env_name}_PASSWORD={password_hash}")
    print(f"\nAlso set your username:")
    print(f"  export {config.const.env_name}_USERNAME='your_username'")
    print(f"\nThen restart the application to apply the changes.\n")
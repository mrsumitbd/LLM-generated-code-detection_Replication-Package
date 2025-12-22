import getpass
from passlib.context import CryptContext

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
    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    while True:
        password = getpass.getpass("Enter a new password: ")
        confirm_password = getpass.getpass("Confirm the new password: ")

        if password == confirm_password:
            password_hash = crypt_context.hash(password)
            print("\nGenerated password hash:")
            print(f"export BSM_PASSWORD='{password_hash}'")
            print("\nSet the BSM_PASSWORD environment variable to the above value.")
            print("This, along with the BSM_USERNAME environment variable, will secure access to the web interface.")
            break
        else:
            print("Passwords do not match. Please try again.")
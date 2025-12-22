import sys
import getpass
from typing import Optional

# Import the application's configured CryptContext.
# The exact import path may vary; adjust if necessary.
try:
    from .config import crypt_context  # type: ignore
except Exception:
    # Fallback: create a default CryptContext if not available.
    from passlib.context import CryptContext
    crypt_context = CryptContext(
        schemes=["bcrypt"],
        default="bcrypt",
        bcrypt__rounds=12,
    )


def generate_password_hash_command() -> Optional[str]:
    """
    Generates a bcrypt hash for a given password, for Web UI authentication.

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
    print("=== Generate BSM Password Hash ===")
    print("You will be prompted to enter a new password twice.")
    print("The password will not be displayed on the screen for security.")
    print("After confirmation, a bcrypt hash will be generated.")
    print()

    try:
        while True:
            pwd = getpass.getpass("Enter new password: ")
            if not pwd:
                print("Password cannot be empty. Please try again.")
                continue
            confirm = getpass.getpass("Confirm new password: ")
            if pwd != confirm:
                print("Passwords do not match. Please try again.\n")
                continue
            break
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return None

    # Generate the hash
    try:
        pwd_hash = crypt_context.hash(pwd)
    except Exception as exc:
        print(f"Error generating hash: {exc}")
        return None

    print("\n=== Password Hash Generated ===")
    print("Use the following hash as the value for the BSM_PASSWORD environment variable:")
    print()
    print(f"BSM_PASSWORD={pwd_hash}")
    print()
    print("Example (Linux/macOS):")
    print(f"export BSM_PASSWORD='{pwd_hash}'")
    print("Example (Windows PowerShell):")
    print(f"$env:BSM_PASSWORD = '{pwd_hash}'")
    print()
    print("You can now restart the web UI to apply the new credentials.")
    return pwd_hash
def generate_password_hash_command():
    import getpass
    from passlib.context import CryptContext

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    print("Enter a new password:")
    password = getpass.getpass()

    print("Confirm the password:")
    confirm_password = getpass.getpass()

    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    hashed_password = context.hash(password)
    print("Generated bcrypt hash:")
    print(hashed_password)
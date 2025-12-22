import nox

def lint_fix(session: nox.Session) -> None:
    """
    Run linting and auto‑formatting tools on the repository.

    This helper installs the required tools and then applies them to the
    source tree.  It is intended to be used as a nox task.

    The order of operations is:
        1. Install black, isort and flake8.
        2. Run black to format the code.
        3. Run isort to sort imports.
        4. Run flake8 to report any remaining linting issues.

    Parameters
    ----------
    session : nox.Session
        The nox session object used to run commands.
    """
    # Install the tools that will be used for linting and formatting.
    session.install("black", "isort", "flake8")

    # Format the code with black.
    session.run("black", ".")

    # Sort imports with isort.
    session.run("isort", ".")

    # Run flake8 to report any remaining linting issues.
    session.run("flake8", ".")
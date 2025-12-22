import nox

def lint_fix(session: nox.Session) -> None:
    """Fix linting issues using ruff."""
    session.install("ruff")
    session.run("ruff", "check", "--fix", ".")
    session.run("ruff", "format", ".")
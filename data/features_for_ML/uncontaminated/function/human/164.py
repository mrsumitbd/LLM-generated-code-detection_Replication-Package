import nox

def lint_fix(session: nox.Session) -> None:
    session.install("isort", "ruff", "pre-commit", "autoflake")
    session.run("ruff", "check", "--fix")
    session.run("isort", ".")
    session.run("pre-commit", "run", "--all-files")
    session.run("autoflake", "--in-place", "--remove-all-unused-imports", "--remove-unused-variables")
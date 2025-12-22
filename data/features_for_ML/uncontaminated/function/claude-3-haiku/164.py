def lint_fix(session: nox.Session) -> None:
    session.install("black", "flake8", "isort")
    session.run("black", ".", "--check")
    session.run("flake8", ".")
    session.run("isort", ".", "--check-only", "--diff")
    session.run("black", ".")
    session.run("isort", ".")
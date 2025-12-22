def lint_fix(session: nox.Session) -> None:
    session.install("flake8")
    session.run("flake8", "your_python_script.py")
from pathlib import Path

from invoke import task


@task
def lint(c):
    c.run("poetry run flake8 .", echo=True, pty=True)


@task
def format(c, fix=False):
    check = "" if fix else "--check"
    c.run(f"poetry run black {check} .", echo=True, pty=True)


@task
def typecheck(c, warn=True):
    repo = Path(".")
    tc = repo / "tamr_client"
    tests = repo / "tests"
    pkgs = [
        tc / "attributes",
        tests / "attributes",
        tc / "datasets",
        tests / "datasets",
    ]
    for pkg in pkgs:
        pyfiles = " ".join(str(pyfile) for pyfile in pkg.glob("**/*.py"))
        c.run(f"poetry run mypy {pyfiles}", echo=True, pty=True, warn=warn)


@task
def test(c):
    c.run("poetry run pytest", echo=True, pty=True)


@task
def docs(c):
    c.run("poetry run sphinx-build -b html docs docs/_build -W", echo=True, pty=True)

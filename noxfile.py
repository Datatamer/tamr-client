from pathlib import Path

import nox

nox.options.reuse_existing_virtualenvs = True


def _find_packages(path: Path):
    for pkg in path.iterdir():
        if pkg.is_dir() and len(list(pkg.glob("**/*.py"))) >= 1:
            yield pkg


@nox.session(python="3.6")
def lint(session):
    session.run("poetry", "install", external=True)
    session.run("flake8", "--extend-exclude=.nox", ".")


@nox.session(python="3.6")
def format(session):
    session.run("poetry", "install", external=True)
    if "--fix" in session.posargs:
        session.run("black", ".")
    else:
        session.run("black", ".", "--check")


@nox.session(python="3.6")
def typecheck(session):
    session.run("poetry", "install", external=True)
    repo = Path(".")

    tc = repo / "tamr_client"
    session.run("mypy", "--package", str(tc))

    tc_tests = [str(x) for x in (repo / "tests" / "tamr_client").glob("**/*.py")]
    session.run("mypy", *tc_tests)


@nox.session(python=["3.6", "3.7", "3.8"])
def test(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", *session.posargs, env={"TAMR_CLIENT_BETA": "1"})


@nox.session(python="3.6")
def docs(session):
    # RTD uses pip for managing dependencies, so we mirror that approach
    session.install(".")
    session.install("-r", "docs/requirements.txt")
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "docs",
        "docs/_build",
        "-W",
        env={"TAMR_CLIENT_BETA": "1"},
    )

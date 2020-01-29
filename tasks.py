from invoke import task


@task
def lint(c):
    c.run("poetry run flake8 .", echo=True, pty=True)


@task
def format(c):
    c.run("poetry run black --check .", echo=True, pty=True)


@task
def test(c):
    c.run("poetry run pytest", echo=True, pty=True)


@task
def docs(c):
    c.run("poetry run sphinx-build -b html docs docs/_build -W", echo=True, pty=True)

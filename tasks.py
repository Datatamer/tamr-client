from invoke import task


@task
def lint(c):
    c.run("poetry run flake8 .", echo=True, pty=True)


@task
def format(c, fix=False):
    check = "" if fix else "--check"
    c.run(f"poetry run black {check} .", echo=True, pty=True)


@task
def test(c):
    c.run("poetry run pytest", echo=True, pty=True)


@task
def docs(c):
    c.run("poetry run sphinx-build -b html docs docs/_build -W", echo=True, pty=True)

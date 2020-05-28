# Run and Build

This project uses [nox](https://nox.thea.codes/en/stable/).

Since `nox` will be running inside of a `poetry` environment (to guarantee you are running the same version of `nox` as everyone else), we recommend adding the following alias to your `.bashrc` / `.zshrc` to save you some keystrokes:

```sh
alias prn='poetry run nox'
```

To run all checks:

```sh
prn # with alias
poetry run nox # without alias
```

## Linting & Formatting

To run linter:

```sh
prn -s lint # with alias
poetry run nox -s lint # without alias
```

To run formatter:

```sh
prn -s format # with alias
poetry run nox -s format # without alias
```

Run the formatter with the `--fix` flag to autofix formatting:

```sh
prn -s format -- --fix # with alias
poetry run nox -s format -- --fix # without alias
```

## Typechecks

To run typechecks:

```sh
prn -s typecheck # with alias
poetry run nox -s typecheck # without alias
```

## Tests

To run all tests:

```sh  
prn -s test # with alias
poetry run nox -s test # without alias
```

---

To run tests for a specific Python version e.g. 3.6:

```sh
prn -s test-3.6 # with alias
poetry run nox -s test-3.6 # without alias
```

See [`nox --list`](https://nox.thea.codes/en/stable/tutorial.html#selecting-which-sessions-to-run) for more details.

---

To run specific tests, see [these pytest docs](https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests) and pass `pytest` args after `--` e.g.:

```sh
prn -s test -- tests/unit/test_attribute.py
```


## Docs

To build the docs:

```sh
prn -s docs # with alias
poetry run nox -s docs # without alias
```

After docs are build, view them by:

```sh
open -a 'firefox' docs/_build/index.html # open in Firefox
open -a 'Google Chrome' docs/_build/index.html # open in Chrome
```

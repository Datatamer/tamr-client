# Run and Build

This project uses [invoke](http://www.pyinvoke.org/) as its task runner.

Since `invoke` will be running inside of a `poetry` environment, we recommend adding the following alias to your `.bashrc` / `.zshrc` to save you some keystrokes:

```sh
alias pri='poetry run invoke'
```

## Tests

To run all tests:

```sh  
pri test # with alias
poetry run invoke test # without alias
```

To run specific tests, see [these pytest docs](https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests) and run `pytest` explicitly:

```sh
poetry run pytest tests/unit/test_attribute.py
```

## Linting & Formatting

To run linter:

```sh
pri lint # with alias
poetry run invoke lint # without alias
```

To run formatter:

```sh
pri format # with alias
poetry run invoke format # without alias
```

Run the formatter with the `--fix` flag to autofix formatting:

```sh
pri format --fix # with alias
poetry run invoke format --fix # without alias
```

## Docs

To build the docs:

```sh
pri docs # with alias
poetry run invoke docs # without alias
```

After docs are build, view them by:

```sh
    open -a 'firefox' docs/_build/index.html # open in Firefox
    open -a 'Google Chrome' docs/_build/index.html # open in Chrome
```

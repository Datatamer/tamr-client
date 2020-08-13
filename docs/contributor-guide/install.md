# Installation

### Prerequisites

1. Install [build dependencies for pyenv](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
2. Install [pyenv](https://github.com/pyenv/pyenv#installation)
3. Install [poetry](https://python-poetry.org/docs/#installation)

### Clone + install

1. Clone your fork and `cd` into the project:

    ```sh
    git clone https://github.com/<your-github-username>/tamr-client
    cd tamr-client
    ```

2. Install all Python versions in [.python-version](https://github.com/Datatamer/tamr-client/blob/master/.python-version):

    [Dev tasks](dev-tasks) will use these Python versions.

    ```sh
    # run `pyenv install` for each line in `.python-version`
    cat .python-version | xargs -L 1 pyenv install
    ```

3. Install project dependencies via `poetry`:

    ```sh
    poetry install
    ```

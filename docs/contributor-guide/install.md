# Install

This project uses `pyenv` and `poetry`.
If you do not have these installed, checkout the [toolchain guide](toolchain).

---

1. Clone your fork and `cd` into the project:

    ```sh
    git clone https://github.com/<your-github-username>/tamr-client
    cd tamr-client
    ```

2. Set a Python version for this project. Must be Python 3.6+ (e.g. `3.7.3`):

    ```sh
    pyenv local 3.7.3
    ```

3. Check that your Python version matches the version specified in `.python-version`:

    ```sh
    cat .python-version
    python --version
    ```

4. Install dependencies via `poetry`:

    ```sh
    poetry install
    ```

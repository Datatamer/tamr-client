# Toolchain

This project uses `poetry` as its package manager. For details on `poetry`,
see the [official documentation](https://poetry.eustace.io/).

  1. Install [pyenv](https://github.com/pyenv/pyenv#installation>):

      ```sh
      curl https://pyenv.run | bash
      ```

  2. Use `pyenv` to install a compatible Python version (`3.6` or newer; e.g. `3.7.3`):

      ```sh
      pyenv install 3.7.3
      ```

  3. Set that Python version to be your version for this project(e.g. `3.7.3`):

      ```sh
      pyenv shell 3.7.3
      python --version # check that version matches your specified version
      ```

  4. Install `poetry` as [described here](https://poetry.eustace.io/docs/#installation):

      ```sh
      curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
      ```

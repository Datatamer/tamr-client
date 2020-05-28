# Toolchain

This project uses `poetry` as its package manager. For details on `poetry`,
see the [official documentation](https://poetry.eustace.io/).

  1. Install [pyenv](https://github.com/pyenv/pyenv#installation>):

      ```sh
      curl https://pyenv.run | bash
      ```

  2. Use `pyenv` to install all Python versions in [.python-version](https://github.com/Datatamer/tamr-client/blob/master/.python-version):

      [Automated tests](run-and-build) will use these Python versions.

      ```sh
      cd tamr-client/ # or wherever you cloned Datatamer/tamr-client

      # run `pyenv install` for each line in `.python-version`
      cat .python-version | xargs -L 1 pyenv install
      ```

  4. Install `poetry` with `python` 3.6+ as [described here](https://poetry.eustace.io/docs/#installation):

      ```sh
      python --version # check that version is 3.6.9
      curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
      ```

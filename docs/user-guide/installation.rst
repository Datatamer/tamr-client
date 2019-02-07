Installation
============

Installation is as simple as::

  pip install tamr-unify-client

.. note::
  We recommend you use a virtual environment for your project and install the
  Python Client into that virtual environment.

  You can create a virtual environment with Python 3 via::

    python3 -m venv my-venv

  For more, see `The Hitchhiker's Guide to Python <https://docs.python-guide.org/dev/virtualenvs/>`_ .

Offline installs
----------------

First, download ``tamr-unify-client`` and its dependencies on a machine with online access to PyPI:

  pip download tamr-unify-client -d tamr-unify-client-requirements
  zip -r tamr-unify-client-requirements.zip tamr-unify-client-requirements

Then, ship the ``.zip`` file to the target machine where you want ``tamr-unify-client`` installed.
You can do this via email, cloud drives, ``scp`` or any other mechanism.

Finally, install ``tamr-unify-client`` from the saved dependencies:

  unzip tamr-unify-client-requirements.zip
  pip install --no-index --find-links=tamr-unify-client-requirements tamr-unify-client

If you are not using a virtual environment, you may need to specify the ``--user`` flag
if you get permissions errors:

  pip install --user --no-index --find-links=tamr-unify-client-requirements tamr-unify-client

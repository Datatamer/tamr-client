Secure Credentials
==================

This section discusses ways to pass credentials securely to
:class:`~tamr_unify_client.auth.UsernamePasswordAuth`. Specifically, you **should
not** hardcode your password(s) in your source code. Instead, you should use
environment variables or secure files to store your credentials and
simple Python code to read your credentials.

Environment variables
---------------------

You can use ``os.environ`` to read in your credentials from environment variables::

  # my_script.py
  import os

  from tamr_unify_client.auth import UsernamePasswordAuth

  username = os.environ['UNIFY_USERNAME'] # replace with your username environment variable name
  password = os.environ['UNIFY_PASSWORD'] # replace with your password environment variable name

  auth = UsernamePasswordAuth(username, password)


You can pass in the environment variables from the terminal by including them
before your command::

  UNIFY_USERNAME="my Unify username" UNIFY_PASSWORD="my Unify password" python my_script.py

You can also create an ``.sh`` file to store your environment variables and
simply ``source`` that file before running your script.


Config files
------------

You can also store your credentials in a secure credentials file::

  # credentials.yaml
  ---
  username: "my unify username"
  password: "my unify password"

Then ``pip install pyyaml`` read the credentials in your Python code::

  # my_script.py
  from tamr_unify_client.auth import UsernamePasswordAuth
  import yaml

  creds = yaml.load("path/to/credentials.yaml") # replace with your credentials.yaml path

  auth = UsernamePasswordAuth(creds.username, creds.password)

As in this example, we recommend you use YAML as your format since YAML has
support for comments and is more human-readable than JSON.

.. important::
  You **should not** check these credentials files into your version
  control system (e.g. ``git``). Do not share this file with anyone who should
  not have access to the password stored in it.

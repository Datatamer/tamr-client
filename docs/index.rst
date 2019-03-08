Tamr Unify - Python Client
==========================

Version: |release| | `View on Github <https://github.com/Datatamer/unify-client-python>`_

Example
-------

::

  from tamr_unify_client import Client
  from tamr_unify_client.auth import UsernamePasswordAuth
  import os

  # grab credentials from environment variables
  username = os.environ['UNIFY_USERNAME']
  password = os.environ['UNIFY_PASSWORD']
  auth = UsernamePasswordAuth(username, password)

  host = 'localhost' # replace with your Tamr Unify host
  unify = Client(auth, host=host)

  # programmatically interace with Tamr Unify!
  # e.g. refresh your project's Unified Dataset
  project = unify.projects.by_resource_id('3')
  ud = project.unified_dataset()
  op = ud.refresh()
  assert op.succeeded()

User Guide
----------

.. toctree::
  :maxdepth: 2

  user-guide/installation
  user-guide/quickstart
  user-guide/secure-credentials
  user-guide/workflows
  user-guide/advanced-usage
  user-guide/faq

Contributor Guide
-----------------

.. toctree::
  :maxdepth: 2

  contributor-guide

Developer Interface
-------------------

.. toctree::
  :maxdepth: 2

  developer-interface

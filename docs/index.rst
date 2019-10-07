Tamr - Python Client
==========================

Version: |release| | `View on Github <https://github.com/Datatamer/tamr-client>`_

Example
-------

::

  from tamr_unify_client import Client
  from tamr_unify_client.auth import UsernamePasswordAuth
  import os

  # grab credentials from environment variables
  username = os.environ['TAMR_USERNAME']
  password = os.environ['TAMR_PASSWORD']
  auth = UsernamePasswordAuth(username, password)

  host = 'localhost' # replace with your Tamr host
  tamr = Client(auth, host=host)

  # programmatically interace with Tamr!
  # e.g. refresh your project's Unified Dataset
  project = tamr.projects.by_resource_id('3')
  ud = project.unified_dataset()
  op = ud.refresh()
  assert op.succeeded()

User Guide
----------

.. toctree::
  :maxdepth: 2

  user-guide/faq
  user-guide/installation
  user-guide/quickstart
  user-guide/secure-credentials
  user-guide/workflows
  user-guide/spec
  user-guide/geo
  user-guide/advanced-usage

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

Advanced Usage
==============

Asynchronous Operations
-----------------------

You can opt-in to an asynchronous interface via the asynchronous keyword argument
for methods that kick-off Unify operations.

E.g.::

  operation = project.unified_dataset().refresh(asynchronous=True)
  # do asynchronous stuff while operation is running
  operation.wait() # hangs until operation finishes
  assert op.succeeded()

Logging API calls
-----------------

It can be useful (e.g. for debugging) to log the API calls made on your behalf
by the Python Client.

You can set up HTTP-API-call logging on any client via
standard `Python logging mechanisms <https://docs.python.org/3/library/logging.html>`_ ::

  from tamr_unify_client import Client
  from unify_api_v1.auth import UsernamePasswordAuth
  import logging

  auth = UsernamePasswordAuth("username", "password")
  unify = Client(auth)

  # Reload the `logging` library since other libraries (like `requests`) already
  # configure logging differently. See: https://stackoverflow.com/a/53553516/1490091
  import imp
  imp.reload(logging)

  logging.basicConfig(
    level=logging.INFO, format="%(message)s", filename=log_path, filemode="w"
  )
  unify.logger = logging.getLogger(name)

By default, when logging is set up, the client will log ``{method} {url} : {response_status}``
for each API call.

You can customize this by passing in a value for ``log_entry``::

  def log_entry(method, url, response):
  # custom logging function
  # use the method, url, and response to construct the logged `str`
  # e.g. for logging out machine-readable JSON:
  import json
  return json.dumps({
    "request": f"{method} {url}",
    "status": response.status_code,
    "json": response.json(),
  })

  # after configuring `unify.logger`
  unify.log_entry = log_entry

Custom HTTP requests
--------------------

We encourage you to use the higher-level, object-oriented interface offered by
the Python Client. If you aren't sure if you need to send low-level HTTP requests,
you probably don't.

But sometimes it's useful to directly send HTTP requests to Unify.

Specific endpoint
^^^^^^^^^^^^^^^^^

The client exposes a ``request`` method with the same interface as ``requests.request``::

  # import Python Client library and configure your client

  unify = Client(auth)
  # do stuff with the `unify` client

  # now I NEED to send a request to a specific endpoint
  response = unify.request('GET', 'some/specific/endpoint')

You can also use the ``get``, ``post``, ``put``, ``delete`` convenience methods::

  # e.g. `get` convenience method
  response = unify.get('some/specific/endpoint')

Custom Host / Port / Base API path
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need to repeatedly send requests to another port or base API path
(i.e. not ``api/versioned/v1``), you can simply instantiate a different client.

Then just call ``request`` as described above::

  # import Python Client library and configure your client

  unify = api.Client(auth)
  # do stuff with the `unify` client

  # now I NEED to send requests to a different host/port/base API path etc..
  # NOTE: in this example, we reuse `auth` from the first client, but we could
  # have made a new Authentication provider if this client needs it.
  custom_client = api.Client(
    auth,
    host="10.10.0.1",
    port=9090,
    base_path="api/some_service",
  )
  response = custom_client.get('some/specific/endpoint')

One-off authenticated request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All of the Python Client Authentication providers adhere to the
``requests.auth.BaseAuth`` interface.

This means that you can pass in an
Authentication provider directly to the ``requests`` library::

  from tamr_unify_client.auth import UsernamePasswordAuth
  import os
  import requests

  username = os.environ['UNIFY_USERNAME']
  password =  os.environ['UNIFY_PASSWORD']
  auth = UsernamePasswordAuth(username, password)

  response = requests.request('GET', 'some/specific/endpoint', auth=auth)

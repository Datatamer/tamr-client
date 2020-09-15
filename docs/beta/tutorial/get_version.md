# Tutorial: Get Tamr version
This tutorial will cover basic Python client usage by guiding you through:
1. Configuring the connection to a Tamr instance
2. Retrieving the version of that instance

## Prerequisites
To complete this tutorial you will need:
- `tamr-unify-client` [installed](../../user-guide/installation)
- access to a Tamr instance, specifically:
  - a username and password that allow you to log in to Tamr
  - the socket address of the instance

The socket address is composed of
1. The protocol, such as `"https"` or `"http"`
2. The host, which may be `"localhost"` if the instance is deployed from the same machine from which your Python code will be run
3. The port at which you access the Tamr user interface, typically `9100`

When you view the Tamr user interface in a browser, the url is `<protocol>://<host>:<port>`. If the port is missing, the URL is simply `<protocol>://host`.

## Steps
### The Session
The Tamr Python client uses a `Session` to persist the user's authentication details across requests made to the server where Tamr is hosted.

A `Session` carries authentication credentials derived from a username and password, and is not explicitly tied to any single Tamr instance. For more details, see the documentation for the [Requests library](https://requests.readthedocs.io/en/master/user/advanced/#session-objects).

 - Use your username and password to create an instance of `tamr_client.UsernamePasswordAuth`.
 - Use the function `tamr_client.session.from.auth` to create a `Session`.
```eval_rst
.. literalinclude:: ../../../examples/get_tamr_version.py
    :language: python
    :lines: 1-9
```
### The Instance
An `Instance` models the installation or instance of Tamr with which a user interacts via the Python client.

- Create an `Instance` using the `protocol`, `host`, and `port` of your Tamr instance.
```eval_rst
.. literalinclude:: ../../../examples/get_tamr_version.py
    :language: python
    :lines: 11-15
```
### Getting the version of Tamr
With the `Session` and `Instance` defined, you can now interact with the API of the Tamr instance.  One simple example is fetching the version of the Tamr software running on the server.

- Use the function `tc.instance.version` and print the returned value.

```eval_rst
.. literalinclude:: ../../../examples/get_tamr_version.py
    :language: python
    :lines: 17
```

All of the above steps can be combined into the following script `get_tamr_version.py`:

```eval_rst
.. literalinclude:: ../../../examples/get_tamr_version.py
    :language: python
```
To run the script via command line:
```bash
TAMR_CLIENT_BETA=1 python get_tamr_version.py
```

If successful, the printed result should be similar to `v2020.016.0`.

Congratulations! This is just the start of what can be done with the Tamr Python client.

To continue learning, see other tutorials and examples.
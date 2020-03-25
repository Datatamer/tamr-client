# Quickstart
## Client configuration

Start by importing the Python Client and authentication provider:
```python
from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
```
Next, create an authentication provider and use that to create an authenticated client:

```python
import os

username = os.environ['TAMR_USERNAME']
password = os.environ['TAMR_PASSWORD']

auth = UsernamePasswordAuth(username, password)
tamr = Client(auth)
```

``` warning:: For security, it's best to read your credentials in from environment variables or secure files instead of hardcoding them directly into your code.

    For more, see `User Guide > Secure Credentials <secure-credentials.html>`_.
```
By default, the client tries to find the Tamr instance on `localhost`. To point to a different host, set the host argument when instantiating the Client.

For example, to connect to `10.20.0.1`:
```python
tamr = Client(auth, host='10.20.0.1')
```

## Top-level collections
The Python Client exposes 2 top-level collections: Projects and Datasets.

You can access these collections through the client and loop over their members
with simple `for`-loops.

E.g.:
```python
for project in tamr.projects:
    print(project.name)

for dataset in tamr.datasets:
    print(dataset.name)
```

## Fetch a specific resource
If you know the identifier for a specific resource, you can ask for it directly via the `by_resource_id` methods exposed by collections.

E.g. To fetch the project with ID `'1'`:
```python
project = tamr.projects.by_resource_id('1')
```
Similarly, if you know the name of a specific resource, you can ask for it directly via the `by_name` methods exposed by collections.

E.g. To fetch the project with name `'Number 1'`:
```python
project = tamr.projects.by_name('Number 1')
```
``` note::
    If working with projects across Tamr instances for migrations or promotions, use external IDs (via ``by_external_id``) instead of name (via ``by_name``).
```

## Resource relationships
Related resources (like a project and its unified dataset) can be accessed through specific methods.

E.g. To access the Unified Dataset for a particular project:
```python
ud = project.unified_dataset()
```

## Kick-off Tamr Operations
Some methods on Model objects can kick-off long-running Tamr operations.

Here, kick-off a "Unified Dataset refresh" operation:
```python
operation = project.unified_dataset().refresh()
assert op.succeeded()
```
By default, the API Clients expose a synchronous interface for Tamr operations.

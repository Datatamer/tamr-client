# Tamr - Python Client

[View on Github](https://github.com/Datatamer/tamr-client)

## Example

```python
from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
import os

# grab credentials from environment variables
username = os.environ['TAMR_USERNAME']
password = os.environ['TAMR_PASSWORD']
auth = UsernamePasswordAuth(username, password)

host = 'localhost' # replace with your Tamr host
tamr = Client(auth, host=host)

# programmatically interact with Tamr!
# e.g. refresh your project's Unified Dataset
project = tamr.projects.by_resource_id('3')
ud = project.unified_dataset()
op = ud.refresh()
assert op.succeeded()
```

## User Guide

  * [FAQ](user-guide/faq)
  * [Install](user-guide/installation)
  * [Quickstart](user-guide/quickstart)
  * [Secure credentials](user-guide/secure-credentials)
  * [Workflows](user-guide/workflows)
  * [Create and update resources](user-guide/spec)
  * [Logging](user-guide/logging)
  * [Geospatial data](user-guide/geo)
  * [Advanced usage](user-guide/advanced-usage)

## Contributor Guide

  * [Contributor guide](contributor-guide)

## Reference

  * [Reference](reference)

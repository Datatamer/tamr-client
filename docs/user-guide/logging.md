# Logging

**IMPORTANT** Make sure to configure logging BEFORE `import`ing from 3rd party
libraries. Logging will use the first configuration it finds, and if a library
configures logging before you, your configuration will be ignored.

---

To configure logging, simply follow the [official Python logging HOWTO](https://docs.python.org/3/howto/logging.html#logging-howto).

For example:
```python
# script.py
import logging

logging.basicConfig(filename="script.log", level=logging.INFO)

# configure logging before other imports

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

auth = UsernamePasswordAuth("my username", "my password")
tamr = Client(auth, host="myhost")

for p in tamr.projects:
    print(p)

for d in tamr.datasets:
    print(d)

# should cause an HTTP error
tamr.get("/invalid/api/path").successful()
```

This will log all API requests made and print the response bodies for any
requests with HTTP error codes.

If you want to **only** configure logging for the Tamr Client:
```python
import logging
logger = logging.getLogger('tamr_unify_client')
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler('tamr-client.log'))

# configure logging before other imports

from tamr_unify_client import Client
from tamr_unify_client import UsernamePasswordAuth

# rest of script goes here
```

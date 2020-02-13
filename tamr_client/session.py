import requests

Session = requests.Session


def from_auth(auth: requests.auth.HTTPBasicAuth, **kwargs) -> Session:
    """Create a new authenticated session

    Args:
        auth: Authentication
    """
    s = requests.Session(**kwargs)
    s.auth = auth
    return s

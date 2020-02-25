import requests

Session = requests.Session


def from_auth(auth: requests.auth.HTTPBasicAuth) -> Session:
    """Create a new authenticated session

    Args:
        auth: Authentication
    """
    s = requests.Session()
    s.auth = auth
    return s

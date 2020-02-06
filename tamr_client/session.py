import requests


def session(auth: requests.auth.HTTPBasicAuth, **kwargs) -> requests.Session:
    """Create a new authenticated session

    Args:
        auth: Authentication
    """
    s = requests.Session(**kwargs)
    s.auth = auth
    return s

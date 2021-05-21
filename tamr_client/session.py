from tamr_client._types import Session
from tamr_client._types.auth import UsernamePasswordAuth


def from_auth(auth: UsernamePasswordAuth) -> Session:
    """Create a new authenticated session

    Args:
        auth: Authentication
    """
    s = Session()
    s._stored_auth = auth
    return s

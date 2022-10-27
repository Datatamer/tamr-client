from typing import Union

from tamr_client._types import Session
from tamr_client._types.auth import JwtTokenAuth, UsernamePasswordAuth


def from_auth(auth: Union[UsernamePasswordAuth, JwtTokenAuth]) -> Session:
    """Create a new authenticated session

    Args:
        auth: Authentication
    """
    s = Session()
    if isinstance(auth, UsernamePasswordAuth):
        s._stored_auth = auth  # flag attempt to set session cookie during requests
    else:
        s.auth = auth  # do not flag to attempt to set session cookie in requests
    return s

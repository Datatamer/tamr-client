from __future__ import absolute_import

from base64 import b64encode

from requests.auth import HTTPBasicAuth
from requests.utils import to_native_string


def _basic_auth_str(username, password):
    auth = f"{username}:{password}"
    encoded = b64encode(auth.encode("latin1"))
    return "BasicCreds " + to_native_string(encoded.strip())


class UsernamePasswordAuth(HTTPBasicAuth):
    """Provides username/password authentication for Tamr.
    Specifically, sets the `Authorization` HTTP header with Tamr's custom `BasicCreds` format.

    :param str username:
    :param str password:

    Usage:
        >>> from tamr_unify_client.auth import UsernamePasswordAuth
        >>> auth = UsernamePasswordAuth('my username', 'my password')
        >>> import tamr_unify_client as api
        >>> unify = api.Client(auth)
    """

    def __init__(self, username, password):
        super(self.__class__, self).__init__(username, password)

    def __call__(self, r):
        r.headers["Authorization"] = _basic_auth_str(self.username, self.password)
        return r

    def __repr__(self):
        # intentionally leave out password (potentially sensitive)
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"username={self.username!r})"
        )

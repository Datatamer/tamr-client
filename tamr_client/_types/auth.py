import base64

import requests


def _basic_auth_str(username, password):
    auth = f"{username}:{password}"
    encoded = base64.b64encode(auth.encode("latin1"))
    return "BasicCreds " + requests.utils.to_native_string(encoded.strip())


class UsernamePasswordAuth(requests.auth.HTTPBasicAuth):
    """Provides username/password authentication for Tamr.

    Sets the `Authorization` HTTP header with Tamr's custom `BasicCreds` format.

    Args:
        username: Tamr username for authentication
        password: Tamr password for authentication

    Example:
        >>> import tamr_client as tc
        >>> auth = tc.UsernamePasswordAuth('my username', 'my password')
        >>> s = tc.Session(auth)
    """

    def __init__(self, username: str, password: str):
        super().__init__(username, password)

    def __call__(self, r):
        r.headers["Authorization"] = _basic_auth_str(self.username, self.password)
        return r

    def __repr__(self):
        # intentionally leave out password (potentially sensitive)
        return (
            f"{type(self).__qualname__}("
            f"username={repr(self.username)}"
            f"password=<redacted>)"
        )


class JwtTokenAuth(requests.auth.AuthBase):
    """Provides JWT authentication for Tamr.

    Specifically, sets the `Authorization` HTTP header with `Bearer` format. This
    feature is only supported in Tamr releases beginning with v2022.010.0

    Args:
        token: The JWT value to be used for authentication

    Usage:
        >>> import tamr_client as tc
        >>> auth = tc.JwtTokenAuth('my token')
        >>> s = tc.Session(auth)
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r

    def __repr__(self):
        # intentionally leave out the token (potentially sensitive)
        return f"{self.__class__.__module__}." f"{self.__class__.__qualname__}()"

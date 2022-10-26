from requests.auth import AuthBase


class JwtTokenAuth(AuthBase):
    """Provides JWT authentication for Tamr.
    Specifically, sets the `Authorization` HTTP header with `Bearer` format. This
    feature is only supported in Tamr releases beginning with v2022.010.0

    Args:
        token: The JWT value to be used for authentication

    Usage:
        >>> from tamr_unify_client.auth import JwtTokenAuth
        >>> auth = JwtTokenAuth('my token')
        >>> import tamr_unify_client as api
        >>> unify = api.Client(auth)
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r

    def __repr__(self):
        # intentionally leave out the token (potentially sensitive)
        return f"{self.__class__.__module__}." f"{self.__class__.__qualname__}()"

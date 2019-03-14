from requests.auth import AuthBase


class TokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "BasicCreds " + self.token
        return r

    def __repr__(self):
        # intentionally leave out the token (potentially sensitive)
        return f"{self.__class__.__module__}." f"{self.__class__.__qualname__}()"

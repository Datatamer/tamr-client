from typing import Optional

import requests

from tamr_client._types.auth import UsernamePasswordAuth


class Session(requests.Session):
    def __init__(self):
        super(self.__class__, self).__init__()
        self._stored_auth: Optional[UsernamePasswordAuth] = None

    def request(self, *args, **kwargs):
        # signature of `requests` requires not naming positional args
        response = super(self.__class__, self).request(*args, **kwargs)
        if response.status_code == 401 and "credentials" in response.text.lower():
            first_response = response
            self._set_auth_cookie(args[1])
            response = super(self.__class__, self).request(*args, **kwargs)
            if response.status_code == 401 and "credentials" in response.text.lower():
                # Login credentials are bad, return original response
                response = first_response
        return response

    def _set_auth_cookie(self, parent_url: str):
        """Fetch and store an auth token for the given client configuration"""
        # No-op if _stored_auth is None
        if self._stored_auth is None:
            return

        # Fetch auth token and store as cookie
        socket_address = parent_url.split("/api/")[0]
        r = self.post(
            socket_address + "/api/versioned/v1/instance:login",
            json={
                "username": self._stored_auth.username,
                "password": self._stored_auth.password,
            },
        )
        if r.status_code == 200:
            auth_token = r.json()["token"]
            self.cookies.set("authToken", auth_token)  # TODO: Set domain for security
            # Clear session auth if cookie is retrieved
            self.auth = None
        else:
            # Set session auth from client auth in case it has been cleared
            # Allow the following call to pass credentials in header
            self.auth = self._stored_auth

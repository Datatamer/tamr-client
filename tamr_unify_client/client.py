from urllib.parse import urljoin

import requests
from requests import Response

from tamr_unify_client.dataset.collection import DatasetCollection
from tamr_unify_client.project.collection import ProjectCollection

# monkey-patch Response.successful


def successful(self):
    """Checks that this response did not encounter an HTTP error (i.e. status code indicates success: 2xx, 3xx).

    :raises :class:`requests.exceptions.HTTPError`: If an HTTP error is encountered.
    :return: The calling response (i.e. ``self``).
    :rtype: :class:`requests.Response`
    """
    self.raise_for_status()
    return self


Response.successful = successful


class Client:
    """Python Client for Unify API. Each client is specific to a specific origin
    (protocol, host, port).

    :param auth: Unify-compatible Authentication provider.
        **Recommended**: use one of the classes described in :ref:`authentication`
    :type auth: :class:`requests.auth.AuthBase`
    :param host: Host address of remote Unify instance (e.g. `10.0.10.0`). Default: `'localhost'`
    :type host: str
    :param protocol: Either `'http'` or `'https'`. Default: `'http'`
    :type protocol: str
    :param port: Unify instance main port. Default: `9100`
    :type port: int
    :param base_path: Base API path. Requests made by this client will be relative to this path. Default: `'api/versioned/v1/'`
    :type base_path: str
    :param session: Session to use for API calls. Default: A new default `requests.Session()`.
    :type session: requests.Session

    Usage:
        >>> import tamr_unify_client as api
        >>> from tamr_unify_client.auth import UsernamePasswordAuth
        >>> auth = UsernamePasswordAuth('my username', 'my password')
        >>> local = api.Client(auth) # on http://localhost:9100
        >>> remote = api.Client(auth, protocol='https', host='10.0.10.0') # on https://10.0.10.0:9100
    """

    def __init__(
        self,
        auth,
        host="localhost",
        protocol="http",
        port=9100,
        base_path="/api/versioned/v1/",
        session=None,
    ):
        self.auth = auth
        self.host = host
        self.protocol = protocol
        self.port = port
        self.base_path = base_path
        self.session = session or requests.Session()

        self._projects = ProjectCollection(self)
        self._datasets = DatasetCollection(self)

        # logging
        self.logger = None
        # https://docs.python.org/3/howto/logging-cookbook.html#implementing-structured-logging

        if not self.base_path.startswith("/"):
            self.base_path = "/" + self.base_path

        if not self.base_path.endswith("/"):
            self.base_path = self.base_path + "/"

        def default_log_entry(method, url, response):
            return f"{method} {url} : {response.status_code}"

        self.log_entry = None

    @property
    def origin(self):
        """HTTP origin i.e. ``<protocol>://<host>[:<port>]``.
        For additional information, see `MDN web docs <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin>`_ .

        :type: str
        """
        return f"{self.protocol}://{self.host}:{self.port}"

    def request(self, method, endpoint, **kwargs):
        """Sends an authenticated request to the server. The URL for the request
        will be ``"<origin>/<base_path>/<endpoint>"``.

        :param method: The HTTP method for the request to be sent.
        :type method: str
        :param endpoint: API endpoint to call (relative to the Base API path for this client).
        :type endpoint: str
        :return: HTTP response
        :rtype: :class:`requests.Response`
        """
        url = urljoin(self.origin + self.base_path, endpoint)
        response = self.session.request(method, url, auth=self.auth, **kwargs)

        # logging
        if self.logger:
            log_message = self.log_entry(method, url, response)
            self.logger.info(log_message)

        return response

    def get(self, endpoint, **kwargs):
        """Calls :func:`~tamr_unify_client.Client.request` with the ``"GET"`` method.
        """
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        """Calls :func:`~tamr_unify_client.Client.request` with the ``"POST"`` method.
        """
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        """Calls :func:`~tamr_unify_client.Client.request` with the ``"PUT"`` method.
        """
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        """Calls :func:`~tamr_unify_client.Client.request` with the ``"DELETE"`` method.
        """
        return self.request("DELETE", endpoint, **kwargs)

    @property
    def projects(self):
        """Collection of all projects on this Unify instance.

        :return: Collection of all projects.
        :rtype: :class:`~tamr_unify_client.project.collection.ProjectCollection`
        """
        return self._projects

    @property
    def datasets(self):
        """Collection of all datasets on this Unify instance.

        :return: Collection of all datasets.
        :rtype: :class:`~tamr_unify_client.dataset.collection.DatasetCollection`
        """
        return self._datasets

    def __repr__(self):
        # Show only the type `auth` to mitigate any security concerns.
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"host={self.host!r}, "
            f"protocol={self.protocol!r}, "
            f"port={self.port!r}, "
            f"base_path={self.base_path!r}, "
            f"auth={type(self.auth).__name__})"
        )

import requests

from tamr_unify_client.models.dataset.collection import DatasetCollection
from tamr_unify_client.models.project.collection import ProjectCollection


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
    :param base_path: Base API path. Requests made by this client will be relative to this path. Default: ``"api/versioned/v1"``
    :type base_path: str

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
        base_path="api/versioned/v1",
    ):
        self.auth = auth
        self.host = host
        self.protocol = protocol
        self.port = port
        self.base_path = base_path

        self._projects = ProjectCollection(self)
        self._datasets = DatasetCollection(self)

        # logging
        self.logger = None
        # https://docs.python.org/3/howto/logging-cookbook.html#implementing-structured-logging
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
        will be ``"<origin>/<base_path>/<endpoint"``.

        :param method: The HTTP method for the request to be sent.
        :type method: str
        :param endpoint: API endpoint to call (relative to the Base API path for this client).
        :type endpoint: str
        :return: HTTP response
        :rtype: :class:`requests.Response`
        """
        url = "/".join([self.origin, self.base_path, endpoint])
        response = requests.request(method, url, auth=self.auth, **kwargs)

        # logging
        if self.logger:
            log_message = self.log_entry(method, url, response)
            self.logger.info(log_message)

        return response

    def request_json(self, method, endpoint, **kwargs):
        """Same as :func:`~tamr_unify_client.client.Client.request`, except it
        raises HTTP errors as exceptions and extracts the response body as JSON.

        :param method: The HTTP method for the request to be sent.
        :type method: str
        :param endpoint: API endpoint to call (relative to the Base API path for this client).
        :type endpoint: str
        :raises :class:`requests.HTTPError`: If an HTTP error occurred.
        :return: Response body parsed as JSON.
        :rtype: :py:class:`dict`
        """
        response = self.request(method, endpoint, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_json(self, endpoint, **kwargs):
        """Calls :func:`~tamr_unify_client.Client.request_json` with the ``"GET"`` method.
        """
        return self.request_json("GET", endpoint, **kwargs)

    def post_json(self, endpoint, **kwargs):
        """Calls :func:`~tamr_unify_client.Client.request_json` with the ``"POST"`` method.
        """
        return self.request_json("POST", endpoint, **kwargs)

    def put_json(self, endpoint, **kwargs):
        """Calls :func:`~tamr_unify_client.Client.request_json` with the ``"PUT"`` method.
        """
        return self.request_json("PUT", endpoint, **kwargs)

    def delete_json(self, endpoint, **kwargs):
        """Calls :func:`~tamr_unify_client.Client.request_json` with the ``"DELETE"`` method.
        """
        return self.request_json("DELETE", endpoint, **kwargs)

    @property
    def projects(self):
        """Collection of all projects on this Unify instance.

        :return: Collection of all projects.
        :rtype: :class:`~tamr_unify_client.models.ProjectCollection`
        """
        return self._projects

    @property
    def datasets(self):
        """Collection of all datasets on this Unify instance.

        :return: Collection of all datasets.
        :rtype: :class:`~tamr_unify_client.models.DatasetCollection`
        """
        return self._datasets

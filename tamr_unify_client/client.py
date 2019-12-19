import logging
from typing import Optional
from urllib.parse import urljoin

import requests
import requests.auth
import requests.exceptions

from tamr_unify_client.dataset.collection import DatasetCollection
from tamr_unify_client.project.collection import ProjectCollection

logger = logging.getLogger(__name__)


def successful(response: requests.Response) -> requests.Response:
    """Ensure response does not contain an HTTP error.

    Delegates to :func:`requests.Response.raise_for_status`

    Returns:
        The response being checked.

    Raises:
        requests.exceptions.HTTPError: If an HTTP error is encountered.
    """
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error code response body: {e.response.text}")
        raise e
    return response


# monkey-patch requests.Response.successful
requests.Response.successful = successful


def _default_response_message(response: requests.Response) -> str:
    req = response.request
    return f"{req.method} {response.url} : {response.status_code}"


class Client:
    """Python Client for Tamr API.

    Each client is specific to a specific origin (protocol, host, port).

    Args:
        auth: Tamr-compatible Authentication provider.

            **Recommended**: use one of the classes described in :ref:`authentication`
        host: Host address of remote Tamr instance (e.g. ``'10.0.10.0'``)
        protocol: Either ``'http'`` or ``'https'``
        port: Tamr instance main port
        base_path: Base API path. Requests made by this client will be relative to this path.
        session: Session to use for API calls. If none is provided, will use a new :class:`requests.Session`.

    Example:
        >>> from tamr_unify_client import Client
        >>> from tamr_unify_client.auth import UsernamePasswordAuth
        >>> auth = UsernamePasswordAuth('my username', 'my password')
        >>> tamr_local = Client(auth) # on http://localhost:9100
        >>> tamr_remote = Client(auth, protocol='https', host='10.0.10.0') # on https://10.0.10.0:9100
    """

    def __init__(
        self,
        auth: requests.auth.AuthBase,
        host: str = "localhost",
        protocol: str = "http",
        port: int = 9100,
        base_path: str = "/api/versioned/v1/",
        session: Optional[requests.Session] = None,
    ):
        self.auth = auth
        self.host = host
        self.protocol = protocol
        self.port = port
        self.base_path = base_path
        self.session = session or requests.Session()

        self._projects = ProjectCollection(self)
        self._datasets = DatasetCollection(self)

        if not self.base_path.startswith("/"):
            self.base_path = "/" + self.base_path

        if not self.base_path.endswith("/"):
            self.base_path = self.base_path + "/"

        self.response_message = _default_response_message

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
        logger.info(self.response_message(response))
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
        """Collection of all projects on this Tamr instance.

        :return: Collection of all projects.
        :rtype: :class:`~tamr_unify_client.project.collection.ProjectCollection`
        """
        return self._projects

    @property
    def datasets(self):
        """Collection of all datasets on this Tamr instance.

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

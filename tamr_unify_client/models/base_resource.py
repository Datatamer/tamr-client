from abc import ABC as AbstractBaseClass


class BaseResource(AbstractBaseClass):
    """Base class for client-side resources.

    :param :class:`~tamr_unify_client.Client` client: Delegate underlying API calls to this client.
    :param :py:class:`dict` data: JSON data received from server for this resource
    :param str alias: API alias for this resource.
    | If set to ``None``, the ``api_path`` of this instance will be set to ``data["relativeId"]``.
    | Default: ``None``.
    """

    def __init__(self, client, data, alias=None):
        self.client = client
        self._data = data
        self.api_path = alias or data["relativeId"]

    @classmethod
    def from_data(cls, client, data, api_path=None):
        return cls(client, data, api_path)

    @property
    def relative_id(self):
        """:type: str"""
        return self._data["relativeId"]

    @property
    def resource_id(self):
        """:type: str"""
        return self.relative_id.split("/")[-1]

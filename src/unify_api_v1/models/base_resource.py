from abc import abstractmethod, ABC as AbstractBaseClass
from google.protobuf.json_format import Parse
import json


class BaseResource(AbstractBaseClass):
    """Base class for client-side resources.

    :param :class:`unify_api_v1.Client` client: Delegate underlying API calls to this client.
    :param :py:class:`dict` data: JSON data received from server for this resource
    :param str alias: API alias for this resource.
    | If set to ``None``, the ``api_path`` of this instance will be set to ``data.relative_id``.
    | Default: ``None``.
    """

    def __init__(self, client, data, alias=None):
        self.client = client
        self.data = data
        self.api_path = alias or data.relative_id

    @classmethod
    def from_data(cls, client, data, api_path=None):
        return cls(client, data, api_path)

    @classmethod
    @abstractmethod
    def from_json(cls, client, resource_json, protobuf_class, api_path=None):
        data = Parse(json.dumps(resource_json), protobuf_class())
        return cls.from_data(client, data, api_path)

    @property
    def relative_id(self):
        """:type: str"""
        return self.data.relative_id

    @property
    def resource_id(self):
        """:type: str"""
        return self.relative_id.split("/")[-1]

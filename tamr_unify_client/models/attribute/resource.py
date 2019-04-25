from tamr_unify_client.models.attribute.type import AttributeType
from tamr_unify_client.models.base_resource import BaseResource


class Attribute(BaseResource):
    """
    A Unify Attribute.

    See https://docs.tamr.com/reference#attribute-types
    """

    @classmethod
    def from_json(cls, client, data, api_path):
        return super().from_data(client, data, api_path)

    @property
    def relative_id(self):
        return self.api_path

    @property
    def name(self):
        """:type: str"""
        return self._data.get("name")

    @property
    def description(self):
        """:type: str"""
        return self._data.get("description")

    @property
    def type(self):
        """:type: :class:`~tamr_unify_client.models.attribute.type.AttributeType`"""
        alias = self.api_path + "/type"
        type_json = self._data.get("type")
        return AttributeType.from_data(self.client, type_json, alias)

    @property
    def is_nullable(self):
        """:type: bool"""
        return self._data.get("isNullable")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r})"
        )

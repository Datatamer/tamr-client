from tamr_unify_client.attribute.type import AttributeType
from tamr_unify_client.base_resource import BaseResource


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
        """:type: str"""
        # api_path is alias when it exists, and relative_id when it does not.
        # this distinction is useful for things like refreshing a unified dataset,
        # where using the relative_id would hit
        #   /datasets/{id}:refresh
        # rather than
        #   /projects/{id}/unifiedDataset:refresh.
        # Since attributes don't currently have that kind of aliasing,
        # using api_path is always correct.
        # If attributes ever get aliased, this will need to be updated.
        # This is confusing; there's an RFC for suggestions to improve this
        # #64 https://github.com/Datatamer/unify-client-python/issues/64
        # "Conflation between 'api_path', 'relative_id' / 'relativeId', and
        # BaseResource ctor 'alias'"
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
        """:type: :class:`~tamr_unify_client.attribute.type.AttributeType`"""
        type_json = self._data.get("type")
        return AttributeType(type_json)

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

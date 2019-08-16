from copy import deepcopy

from tamr_unify_client.attribute.type import AttributeType
from tamr_unify_client.base_resource import BaseResource


class Attribute(BaseResource):
    """
    A Tamr Attribute.

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

    def spec(self):
        """Returns a spec representation of this attribute.

        :return: The attribute spec.
        :rtype: :class:`~tamr_unify_client.attribute.resource.AttributeSpec`
        """
        return AttributeSpec.of(self)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r})"
        )


class AttributeSpec:
    """A representation of the server view of an attribute"""

    def __init__(self, client, data, api_path):
        self._data = data
        self.client = client
        self.api_path = api_path

    @staticmethod
    def of(resource):
        """Creates an attribute spec from an attribute.

        :param resource: The existing attribute.
        :type resource: :class:`~tamr_unify_client.attribute.resource.Attribute`
        :return: The corresponding attribute spec.
        :rtype: :class:`~tamr_unify_client.attribute.resource.AttributeSpec`
        """
        return AttributeSpec(
            resource.client, deepcopy(resource._data), resource.api_path
        )

    @staticmethod
    def new():
        """Creates a blank spec that could be used to construct a new attribute.

        :return: The empty spec.
        :rtype: :class:`~tamr_unify_client.attribute.resource.AttributeSpec`
        """
        return AttributeSpec(None, {}, None)

    def from_data(self, data):
        """Creates a spec with the same client and API path as this one, but new data.

        :param data: The data for the new spec.
        :type data: dict
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.attribute.resource.AttributeSpec`
        """
        return AttributeSpec(self.client, data, self.api_path)

    def to_dict(self):
        """Returns a version of this spec that conforms to the API representation.

        :returns: The spec's dict.
        :rtype: dict
        """
        return deepcopy(self._data)

    def with_name(self, new_name):
        """Creates a new spec with the same properties, updating name.

        :param new_name: The new name.
        :type new_name: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.attribute.resource.AttributeSpec`
        """
        return self.from_data({**self._data, "name": new_name})

    def with_description(self, new_description):
        """Creates a new spec with the same properties, updating description.

        :param new_description: The new description.
        :type new_description: str
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.attribute.resource.AttributeSpec`
        """
        return self.from_data({**self._data, "description": new_description})

    def with_type(self, new_type):
        """Creates a new spec with the same properties, updating type.

        :param new_type: The spec of the new type.
        :type new_type: :class:`~tamr_unify_client.attribute.type.AttributeTypeSpec`
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.attribute.resource.AttributeSpec`
        """
        type_spec = new_type.to_dict()
        return self.from_data({**self._data, "type": type_spec})

    def with_is_nullable(self, new_is_nullable):
        """Creates a new spec with the same properties, updating is nullable.

        :param new_is_nullable: The new is nullable.
        :type new_is_nullable: bool
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.attribute.resource.AttributeSpec`
        """
        return self.from_data({**self._data, "isNullable": new_is_nullable})

    def put(self):
        """Commits the changes and updates the attribute in Tamr.

        :return: The updated attribute.
        :rtype: :class:`~tamr_unify_client.attribute.resource.Attribute`
        """
        updated_attribute = (
            self.client.put(self.api_path, json=self._data).successful().json()
        )
        return Attribute.from_json(self.client, updated_attribute, self.api_path)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dict={self._data!r})"
        )

from tamr_unify_client.models.attribute.resource import Attribute
from tamr_unify_client.models.base_collection import BaseCollection


class AttributeCollection(BaseCollection):
    """Collection of :class:`~tamr_unify_client.models.attribute.resource.Attribute` s.

    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    :param :py:class:`dict` data: JSON data representing this resource
    :param api_path: API path used to access this collection.
        E.g. ``"datasets/1/attributes"``.
    :type api_path: str
    """

    def __init__(self, client, data, api_path):
        super().__init__(client, api_path)
        self._data = data

    @classmethod
    def from_json(cls, client, data, api_path):
        # BaseCollection doesn't really implement from_json / from_data
        # but we pretend it does.
        return AttributeCollection(client, data, api_path)

    def by_resource_id(self, resource_id):
        """Retrieve an attribute by resource ID.

        :param resource_id: The resource ID. E.g. ``"AttributeName"``
        :type resource_id: str
        :returns: The specified attribute.
        :rtype: :class:`~tamr_unify_client.models.attribute.resource.Attribute`
        """
        return self.by_name(resource_id)

    def by_relative_id(self, relative_id):
        """Retrieve an attribute by relative ID.

        :param relative_id: The resource ID. E.g. ``"datasets/1/attributes/AttributeName"``
        :type relative_id: str
        :returns: The specified attribute.
        :rtype: :class:`~tamr_unify_client.models.attribute.resource.Attribute`
        """
        split_id = relative_id.split("/")
        if split_id[:-1] != self.api_path:
            raise ValueError(f"Attribute f{relative_id} is not in collection {self.api_path}")
        resource_id = split_id[-1]
        return self.by_resource_id(resource_id)

    def by_external_id(self, external_id):
        """Retrieve an attribute by external ID.

        Since attributes do not have external IDs, this method is not supported and will
        raise a NotImplementedError.

        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified attribute, if found.
        :rtype: :class:`~tamr_unify_client.models.attribute.resource.Attribute`
        :raises KeyError: If no attribute with the specified external_id is found
        :raises LookupError: If multiple attributes with the specified external_id are found
        """
        raise NotImplementedError("Attributes do not have external_id")

    def stream(self):
        """Stream datasets in this collection. Implicitly called when iterating
        over this collection.

        :returns: Stream of datasets.
        :rtype: Python generator yielding :class:`~tamr_unify_client.models.dataset.resource.Dataset`

        Usage:
            >>> for dataset in collection.stream(): # explicit
            >>>     do_stuff(dataset)
            >>> for dataset in collection: # implicit
            >>>     do_stuff(dataset)
        """
        for resource_json in self._data:
            alias = self.api_path + "/" + resource_json["name"]
            yield Attribute.from_json(self.client, resource_json, alias)

    def by_name(self, attribute_name):
        """Lookup a specific attribute in this collection by exact-match on name.

        :param attribute_name: Name of the desired attribute.
        :type attribute_name: str
        :return: Attribute with matching name in this collection.
        :rtype: :class:`~tamr_unify_client.models.attribute.resource.Attribute`
        :raises KeyError: If no attribute with specified name was found.
        """
        for attribute in self:
            if attribute.name == attribute_name:
                return attribute
        raise KeyError(f"No attribute found with name: {attribute_name}")

    # super.__repr__ is sufficient

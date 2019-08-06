from tamr_unify_client.attribute.resource import Attribute
from tamr_unify_client.base_collection import BaseCollection


class AttributeCollection(BaseCollection):
    """Collection of :class:`~tamr_unify_client.attribute.resource.Attribute` s.

    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    :param api_path: API path used to access this collection.
        E.g. ``"datasets/1/attributes"``.
    :type api_path: str
    """

    def __init__(self, client, api_path):
        super().__init__(client, api_path)

    def by_resource_id(self, resource_id):
        """Retrieve an attribute by resource ID.

        :param resource_id: The resource ID. E.g. ``"AttributeName"``
        :type resource_id: str
        :returns: The specified attribute.
        :rtype: :class:`~tamr_unify_client.attribute.resource.Attribute`
        """
        return super().by_resource_id(self.api_path, resource_id)

    def by_relative_id(self, relative_id):
        """Retrieve an attribute by relative ID.

        :param relative_id: The resource ID. E.g. ``"datasets/1/attributes/AttributeName"``
        :type relative_id: str
        :returns: The specified attribute.
        :rtype: :class:`~tamr_unify_client.attribute.resource.Attribute`
        """
        return super().by_relative_id(Attribute, relative_id)

    def by_external_id(self, external_id):
        """Retrieve an attribute by external ID.

        Since attributes do not have external IDs, this method is not supported and will
        raise a :class:`NotImplementedError` .

        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified attribute, if found.
        :rtype: :class:`~tamr_unify_client.attribute.resource.Attribute`
        :raises KeyError: If no attribute with the specified external_id is found
        :raises LookupError: If multiple attributes with the specified external_id are found
        """
        raise NotImplementedError("Attributes do not have external_id")

    def stream(self):
        """Stream attributes in this collection. Implicitly called when iterating
        over this collection.

        :returns: Stream of attributes.
        :rtype: Python generator yielding :class:`~tamr_unify_client.attribute.resource.Attribute`

        Usage:
            >>> for attribute in collection.stream(): # explicit
            >>>     do_stuff(attribute)
            >>> for attribute in collection: # implicit
            >>>     do_stuff(attribute)
        """
        data = self.client.get(self.api_path).successful().json()
        for resource_json in data:
            alias = self.api_path + "/" + resource_json["name"]
            yield Attribute.from_json(self.client, resource_json, alias)

    def by_name(self, attribute_name):
        """Lookup a specific attribute in this collection by exact-match on name.

        :param attribute_name: Name of the desired attribute.
        :type attribute_name: str
        :return: Attribute with matching name in this collection.
        :rtype: :class:`~tamr_unify_client.attribute.resource.Attribute`
        """
        return super().by_resource_id(self.api_path, attribute_name)

    def create(self, creation_spec):
        """
        Create an Attribute in this collection

        :param creation_spec: Attribute creation specification should be formatted as specified in the `Public Docs for adding an Attribute <https://docs.tamr.com/reference#add-attributes>`_.
        :type creation_spec: dict[str, str]
        :returns: The created Attribute
        :rtype: :class:`~tamr_unify_client.attribute.resource.Attribute`
        """
        data = self.client.post(self.api_path, json=creation_spec).successful().json()
        alias = self.api_path + "/" + creation_spec["name"]
        return Attribute.from_json(self.client, data, alias)

    # super.__repr__ is sufficient

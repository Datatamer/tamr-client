from tamr_unify_client.project.attribute_mapping.resource import AttributeMapping


class AttributeMappingCollection:
    """Collection of :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMapping`
    :param map_url: API path used to access this collection.
    :type api_path: str
    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    """

    def __init__(self, client, api_path):
        self.api_path = api_path
        self.client = client

    def stream(self):
        """Stream items in this collection.
        :returns: Stream of attribute mappings.
        """
        all_maps = self.client.get(self.api_path).successful().json()
        for mapping in all_maps:
            yield AttributeMapping(mapping)

    def by_resource_id(self, resource_id):
        """Retrieve an item in this collection by resource ID.
        :param resource_id: The resource ID.
        :type resource_id: str
        :returns: The specified attribute mapping.
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMapping`
        """
        maps = self.stream()
        for mapping in maps:
            split_id = mapping.resource_id
            if resource_id == split_id:
                return mapping
        raise LookupError("cannot locate mapping from resource ID")

    def by_relative_id(self, relative_id):
        """Retrieve an item in this collection by relative ID.
       :param relative_id: The relative ID.
       :type relative_id: str
       :returns: The specified attribute mapping.
       :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMapping`
       """
        resource_id = relative_id.split("attributeMappings/")[1]
        return self.by_resource_id(resource_id)

    def create(self, creation_spec):
        """Create an Attribute mapping in this collection
        :param creation_spec: Attribute mapping creation specification should be formatted as specified in the
        `Public Docs for adding an AttributeMapping <https://docs.tamr.com/reference#create-an-attribute-mapping>`_.
        :type creation_spec: dict[str, str]
        :returns: The created Attribute mapping
        :rtype: :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMapping`
        """
        data = self.client.post(self.api_path, json=creation_spec).successful().json()
        return AttributeMapping(data)

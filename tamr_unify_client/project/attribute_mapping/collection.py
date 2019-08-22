from tamr_unify_client.project.attribute_mapping.resource import AttributeMapping


class AttributeMappingCollection:
    """Collection of :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMapping`

    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    :param api_path: API path used to access this collection.
    :type api_path: str
    """

    def __init__(self, client, api_path):
        self.client = client
        self.api_path = api_path

    def stream(self):
        """Stream attribute mappings in this collection. Implicitly called when iterating
        over this collection.

        :returns: Stream of attribute mappings.
        :rtype: Python generator yielding :class:`~tamr_unify_client.project.attribute_mapping.resource.AttributeMapping`
        """
        all_maps = self.client.get(self.api_path).successful().json()
        for mapping in all_maps:
            yield AttributeMapping(self.client, mapping)

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
        return AttributeMapping(self.client, data)

    def delete_by_resource_id(self, resource_id):
        """Delete an attribute mapping using its Resource ID.

        :param resource_id: the resource ID of the mapping to be deleted.
        :type resource_id: str
        :returns: HTTP response from the server
        :rtype: :class:`requests.Response`
         """
        path = self.api_path + "/" + resource_id
        response = self.client.delete(path).successful()
        return response

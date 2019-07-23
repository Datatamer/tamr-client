from tamr_unify_client.models.base_collection import BaseCollection
from tamr_unify_client.models.project.attribute_mapping import AttributeMapping


class AttributeMappingCollection(BaseCollection):
    """Collection of :class ~tamr_unify_client.models.project.attribute_mapping.AttributeMapping'
    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    :param resource_json: JSON data representing this resource
    :param api_path: API path used to access this collection.
    E.g. ``"projects/4/attributeMappings/19054-12"``
    :type api_path: str
    """

    def by_relative_id(self, relative_id):
        """Retrieve an attribute mapping by relative ID.
       :param relative_id: The relative ID.
       :type relative_id: str
       :returns: The specified attribute mapping.
       :rtype: :class:`~tamr_unify_client.models.project.attribute_mapping.AttributeMapping`
       """
        return super().by_relative_id(AttributeMapping, relative_id)

    def by_external_id(self, external_id):
        """Retrieve an attribute mapping by external ID.
        Since attributes do not have external IDs, this method is not supported and will
        raise a :class:`NotImplementedError` .
        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified attribute mapping, if found.
        :rtype: :class:`~tamr_unify_client.models.project.attribute_mapping.AttributeMapping`
        :raises KeyError: If no attribute mapping with the specified external_id is found
        :raises LookupError: If multiple attribute mappings with the specified external_id are found
        :raises NotImplementedError: AttributeMapping does not support external_id
        """
        raise NotImplementedError("AttributeMapping does not support external_id")

    def by_resource_id(self, resource_id):
        """Retrieve an attribute mapping by resource ID.
        Since attributes do not have resource IDs, this method is not supported and will
        raise a :class:`NotImplementedError` .
        :param resource_id: The resource ID.
        :type resource_id: str
        :returns: The specified attribute mapping, if found.
        :rtype: :class:`~tamr_unify_client.models.project.attribute_mapping.AttributeMapping`
        :raises KeyError: If no attribute mapping with the specified resource_id is found
        :raises LookupError: If multiple attribute mappings with the specified resource_id are found
        :raises NotImplementedError: AttributeMapping does not support resource_id
        """
        raise NotImplementedError("AttributeMapping does not support resource_id")

    def stream(self):
        """Stream attribute mappings in this collection. Implicitly called when iterating
         over this collection.
         :returns: Stream of attribute mappings.
         :rtype: Python generator yielding :class:`~tamr_unify_client.models.project.attribute_mapping.AttributeMapping`
         Usage:
             >>> for attributeMapping in attribute_mapping__collection.stream(): # explicit
             >>>     do_stuff(attributeMapping)
             >>> for attributeMapping in attribute_mapping__collection: # implicit
             >>>     do_stuff(attributeMapping)
         """

        return super().stream(AttributeMapping)

    def create(self, creation_spec):
        """Create an Attribute mapping in this collection
       :param creation_spec: Attribute mapping creation specification should be formatted as specified in the

       `Public Docs for adding an AttributeMapping <https://docs.tamr.com/reference/#create-an-attribute-mapping>`_.

       :type creation_spec: dict[str, str]
       :returns: The created Attribute mapping
       :rtype: :class:`~tamr_unify_client.models.project.attribute_mapping.AttributeMapping`
       """
        data = self.client.post(self.api_path, json=creation_spec).successful().json()
        return AttributeMapping.from_json(self.client, data)

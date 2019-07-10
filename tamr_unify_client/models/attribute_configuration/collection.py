from tamr_unify_client.models.attribute_configuration.resource import (
    AttributeConfiguration,
)
from tamr_unify_client.models.base_collection import BaseCollection


class AttributeConfigurationCollection(BaseCollection):

    """Collection of :class'tamr_unify_client.models.attribute_configuration.resource.AttributeConfigurations
    :param client: Client for API call delegation.
    :type client: :class:`~tamr_unify_client.Client`
    :param data: JSON data representing this resource
    :type data: dict
    :param api_path: API path used to access this collection.
        E.g. ``"datasets/1/attributeConfigurations"``.
    :type api_path: str
    """

    def __init__(self, client, data, api_path):
        super().__init__(client, api_path)
        self._data = data

    @classmethod
    def from_json(cls, client, data, api_path):
        return AttributeConfigurationCollection(client, data, api_path)

    def by_resource_id(self, resource_id):
        """Retrieve an attribute configuration by resource ID.
        :param resource_id: The resource ID.
        :type resource_id: str
        :returns: The specified attribute configuration.
        :rtype: :class:`~tamr_unify_client.models.attribute_configuration.resource.AttributeConfiguration`
        """
        return super().by_resource_id(self.api_path, resource_id)

    def by_relative_id(self, relative_id):
        """Retrieve an attribute configuration by relative ID.
       :param relative_id: The resource ID.
       :type resource_id: str
       :returns: The specified attribute configuration.
       :rtype: :class:`~tamr_unify_client.models.attribute_configuration.resource.AttributeConfiguration`
       """
        return super().by_relative_id(AttributeConfiguration, relative_id)

    def by_external_id(self, external_id):
        """Retrieve an attribute configuration by external ID.

        Since attributes do not have external IDs, this method is not supported and will
        raise a :class:`NotImplementedError` .

        :param external_id: The external ID.
        :type external_id: str
        :returns: The specified attribute, if found.
        :rtype: :class:`~tamr_unify_client.models.attribute_configuration.resource.AttributeConfiguration`
        :raises KeyError: If no attribute with the specified external_id is found
        :raises LookupError: If multiple attributes with the specified external_id are found
        """
        raise NotImplementedError(
            "Attributes, and therefore attribute configurations, do not have external_id"
        )

    def stream(self):

        """Stream attributes in this collection. Implicitly called when iterating
         over this collection.

         :returns: Stream of attributes.
         :rtype: Python generator yielding :class:`~tamr_unify_client.models.attribute_configuration.resource.AttributeConfiguration`

         Usage:
             >>> for attribute in collection.stream(): # explicit
             >>>     do_stuff(attribute)
             >>> for attribute in collection: # implicit
             >>>     do_stuff(attribute)
         """

        for resource_json in self._data:
            alias = self.api_path + "/" + resource_json["relativeId"]
            yield AttributeConfiguration.from_json(self.client, resource_json, alias)

    def create(self, creation_spec):
        """
       Create an Attribute configuration in this collection

       :param creation_spec: Attribute configuration creation specification should be formatted as specified in the
       `Public Docs for adding an Attribute <https://docs.tamr.com/reference#create-attribute-configurations>`_.
       :type creation_spec: dict[str, str]
       :returns: The created Attribute configurations
       :rtype: :class:`~tamr_unify_client.models.attribute_configuration.resource.AttributeConfigurations`
       """
        data = self.client.post(self.api_path, json=creation_spec).successful().json()
        alias = self.api_path + "/" + creation_spec[0]["relativeId"]
        return AttributeConfiguration.from_json(self.client, data, alias)

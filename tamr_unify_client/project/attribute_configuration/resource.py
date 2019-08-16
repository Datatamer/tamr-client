from copy import deepcopy

from tamr_unify_client.base_resource import BaseResource


class AttributeConfiguration(BaseResource):
    """The configurations of Tamr Attributes.

   See https://docs.tamr.com/reference#the-attribute-configuration-object
   """

    @classmethod
    def from_json(
        cls, client, resource_json, api_path=None
    ) -> "AttributeConfiguration":
        return super().from_data(client, resource_json, api_path)

    @property
    def relative_id(self):
        """:type: str"""
        return self._data.get("relativeId")

    @property
    def id(self):
        """:type: str"""
        return self._data.get("id")

    @property
    def relative_attribute_id(self):
        """:type: str"""
        return self._data.get("relativeAttributeId")

    @property
    def attribute_role(self):
        """:type: str"""
        return self._data.get("attributeRole")

    @property
    def similarity_function(self):
        """:type: str"""
        return self._data.get("similarityFunction")

    @property
    def enabled_for_ml(self):
        """:type: bool"""
        return self._data.get("enabledForMl")

    @property
    def tokenizer(self):
        """:type: str"""
        return self._data.get("tokenizer")

    @property
    def numeric_field_resolution(self):
        """:type: list """
        return self._data.get("numericFieldResolution")

    @property
    def attribute_name(self):
        """:type: str"""
        return self._data.get("attributeName")

    def spec(self):
        """Returns this attribute configuration's spec.

         :return: The spec of this attribute configuration.
         :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
         """
        return AttributeConfigurationSpec.of(self)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"id={self.id!r}, "
            f"relative_attribute_id={self.relative_attribute_id!r}, "
            f"attribute_role={self.attribute_role!r}, "
            f"similarity_function={self.similarity_function!r}, "
            f"enabled_for_ml={self.enabled_for_ml!r}, "
            f"tokenizer={self.tokenizer!r}, "
            f"numeric_field_resolution={self.numeric_field_resolution!r}, "
            f"attribute_name={self.attribute_name!r})"
        )


class AttributeConfigurationSpec:
    """A representation of the server view of an attribute configuration."""

    def __init__(self, client, data, api_path):
        self.client = client
        self._data = data
        self.api_path = api_path

    @staticmethod
    def of(resource):
        """Creates an attribute configuration spec from an attribute configuration.

        :param resource: The existing attribute configuration.
        :type resource: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfiguration`
        :return: The corresponding attribute creation spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return AttributeConfigurationSpec(
            resource.client, deepcopy(resource._data), resource.api_path
        )

    @staticmethod
    def new():
        """Creates a blank spec that could be used to construct a new attribute configuration.

        :return: The empty spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return AttributeConfigurationSpec(None, {}, None)

    def from_data(self, data):
        """Creates a spec with the same client and API path as this one, but new data.

        :param data: The data for the new spec.
        :type data: dict
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return AttributeConfigurationSpec(self.client, data, self.api_path)

    def to_dict(self):
        """Returns a version of this spec that conforms to the API representation.

        :returns: The spec's dict.
        :rtype: dict
        """
        return deepcopy(self._data)

    def with_attribute_role(self, new_attribute_role):
        """Creates a new spec with the same properties, updating attribute role.

        :param new_attribute_role: The new attribute role.
        :type new_attribute_role: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return self.from_data({**self._data, "attributeRole": new_attribute_role})

    def with_similarity_function(self, new_similarity_function):
        """Creates a new spec with the same properties, updating similarity function.

        :param new_similarity_function: The new similarity function.
        :type new_similarity_function: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return self.from_data(
            {**self._data, "similarityFunction": new_similarity_function}
        )

    def with_enabled_for_ml(self, new_enabled_for_ml):
        """Creates a new spec with the same properties, updating enabled for ML.

        :param new_enabled_for_ml: Whether the builder is enabled for ML.
        :type new_enabled_for_ml: bool
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return self.from_data({**self._data, "enabledForMl": new_enabled_for_ml})

    def with_tokenizer(self, new_tokenizer):
        """Creates a new spec with the same properties, updating tokenizer.

        :param new_tokenizer: The new tokenizer.
        :type new_tokenizer: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return self.from_data({**self._data, "tokenizer": new_tokenizer})

    def with_numeric_field_resolution(self, new_numeric_field_resolution):
        """Creates a new spec with the same properties, updating numeric field resolution.

        :param new_numeric_field_resolution: The new numeric field resolution.
        :type new_numeric_field_resolution: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return self.from_data(
            {**self._data, "numericFieldResolution": new_numeric_field_resolution}
        )

    def with_attribute_name(self, new_attribute_name):
        """Creates a new spec with the same properties, updating new attribute name.

        :param new_attribute_name: The new attribute name.
        :type new_attribute_name: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfigurationSpec`
        """
        return self.from_data({**self._data, "attributeName": new_attribute_name})

    def put(self):
        """Updates the attribute configuration on the server.

        :return: The modified attribute configuration.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfiguration`
        """
        new_data = self.client.put(self.api_path, json=self._data).successful().json()
        return AttributeConfiguration.from_json(self.client, new_data, self.api_path)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dict={self._data})"
        )

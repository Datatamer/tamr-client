import copy

from tamr_unify_client.base_resource import BaseResource


class AttributeConfiguration(BaseResource):
    """The configurations of Unify Attributes.

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

    def with_enabled_for_ml(self, toggle):
        """
        Toggles the attribute configuration's enabledForMl field.

        :param toggle: The new value for attribute configuration's enabledForMl field.
        :type toggle: bool
        :return: Updated attribute configuration.
        :rtype: :class: `~tamr_unify_client.project.attribute_configuration.resource.AttributeConfiguration`
        """
        new_attr_config = AttributeConfiguration(self.client, self._data, self.api_path)
        new_attr_config.__dict__ = copy.deepcopy(self.__dict__)
        new_attr_config.__dict__["_data"]["enabledForMl"] = toggle
        return new_attr_config

    def _build(self):
        """
        Creates the new data for attribute configuration.

        :return: Data for the attribute configuration.
        :rtype: JSON
        """
        return self._data

    def put(self):
        """
        Modifies attribute configuration fields with updates requested.

        :return: Modified attribute configuration.
        :rtype: :class:`~tamr_unify_client.project.attribute_configuration.resource.AttributeConfiguration`
        """
        new_data = (
            self.client.put(self.api_path, json=self._build()).successful().json()
        )
        return AttributeConfiguration(self.client, new_data, self.api_path)

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

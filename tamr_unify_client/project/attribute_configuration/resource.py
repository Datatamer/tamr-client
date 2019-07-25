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

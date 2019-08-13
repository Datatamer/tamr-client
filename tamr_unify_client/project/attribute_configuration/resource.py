from tamr_unify_client.base_builder import BaseBuilder
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

    def build(self):
        return AttributeBuilder(self)


class AttributeBuilder(BaseBuilder):
    def with_relative_id(self, new_relative_id):
        return AttributeBuilder(self, relative_id=new_relative_id)

    def with_id(self, new_id):
        return AttributeBuilder(self, id=new_id)

    def with_relative_attribute_id(self, new_relative_attribute_id):
        return AttributeBuilder(self, relative_attribute_id=new_relative_attribute_id)

    def with_attribute_role(self, new_attribute_role):
        return AttributeBuilder(self, attribute_role=new_attribute_role)

    def with_similarity_function(self, new_similarity_function):
        return AttributeBuilder(self, similarity_function=new_similarity_function)

    def with_enabled_for_ml(self, new_enabled_for_ml):
        return AttributeBuilder(self, enabled_for_ml=new_enabled_for_ml)

    def with_tokenizer(self, new_tokenizer):
        return AttributeBuilder(self, tokenizer=new_tokenizer)

    def with_numeric_field_resolution(self, new_numeric_field_resolution):
        return AttributeBuilder(
            self, numeric_field_resolution=new_numeric_field_resolution
        )

    def with_attribute_name(self, new_attribute_name):
        return AttributeBuilder(self, attribute_name=new_attribute_name)

    def _build(self):
        return {
            "relative_id": self.relative_id,
            "id": self.id,
            "relative_attribute_id": self.relative_attribute_id,
            "attribute_role": self.attribute_role,
            "similarity_function": self.similarity_function,
            "enabled_for_ml": self.enabled_for_ml,
            "tokenizer": self.tokenizer,
            "numeric_field_resolution": self.numeric_field_resolution,
            "attribute_name": self.attribute_name,
        }

    def put(self):
        return super().put(AttributeConfiguration)

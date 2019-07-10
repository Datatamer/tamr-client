from tamr_unify_client.models.base_resource import BaseResource


class AttributeConfiguration(BaseResource):
    """
   The configurations of Unify Attributes.

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
    def relativeAttributeId(self):
        """:type: str"""
        return self._data.get("relativeAttributeId")

    @property
    def attributeRole(self):
        """:type: str"""
        return self._data.get("attributeRole")

    @property
    def similarityFunction(self):
        """:type: str"""
        return self._data.get("similarityFunction")

    @property
    def enabledForMl(self):
        """:type: bool"""
        return self._data.get("enabledForMl")

    @property
    def tokenizer(self):
        """:type: str"""
        return self._data.get("tokenizer")

    @property
    def numericFieldResolution(self):
        """:type: array (?) """
        return self._data.get("numericFieldResolution")

    @property
    def attributeName(self):
        """:type: str"""
        return self._data.get("attributeName")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"id={self.id!r}, "
            f"relativeAttributeId={self.relativeAttributeId!r}, "
            f"attributeRole={self.attributeRole!r}, "
            f"similarityFunction={self.similarityFunction!r}, "
            f"enabledForMl={self.enabledForMl!r}, "
            f"tokenizer={self.tokenizer!r}, "
            f"numericFieldResolution={self.numericFieldResolution!r}, "
            f"attributeName={self.attributeName!r})"
        )

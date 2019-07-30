from tamr_unify_client.models.base_resource import BaseResource


class AttributeMapping(BaseResource):
    """
    see https://docs.tamr.com/reference#retrieve-projects-mappings
    """

    @classmethod
    def from_json(cls, client, resource_json, api_path=None) -> "AttributeMapping":
        return super().from_data(client, resource_json, api_path)

    @property
    def id(self):
        """:type: str"""
        return self._data.get("id")

    @property
    def relative_id(self):
        """:type: str"""
        return self._data.get("relativeId")

    @property
    def input_attribute_id(self):
        """:type: str"""
        return self._data.get("inputAttributeId")

    @property
    def relative_input_attribute_id(self):
        """:type: str"""
        return self._data.get("relativeInputAttributeId")

    @property
    def input_dataset_name(self):
        """:type: str"""
        return self._data.get("inputDatasetName")

    @property
    def input_attribute_name(self):
        """:type: str"""
        return self._data.get("inputAttributeName")

    @property
    def unified_attribute_id(self):
        """:type: str"""
        return self._data.get("unifiedAttributeId")

    @property
    def relative_unified_attribute_id(self):
        """:type: str"""
        return self._data.get("relativeUnifiedAttributeId")

    @property
    def unified_dataset_name(self):
        """:type: str"""
        return self._data.get("unifiedDatasetName")

    @property
    def unified_attribute_name(self):
        """:type: str"""
        return self._data.get("unifiedAttributeName")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"id={self.id!r}, "
            f"relative_id={self.relative_id!r}, "
            f"input_attribute_id={self.input_attribute_id!r}, "
            f"relative_input_attribute_id={self.relative_input_attribute_id!r}, "
            f"input_dataset_name={self.input_dataset_name!r}, "
            f"input_attribute_name={self.input_attribute_name!r}, "
            f"unified_attribute_id={self.unified_attribute_id!r}, "
            f"relative_unified_attribute_id={self.relative_unified_attribute_id!r}, "
            f"unified_dataset_name={self.unified_dataset_name!r}, "
            f"unified_attribute_name={self.unified_attribute_name!r})"
        )

class AttributeMapping:
    """see https://docs.tamr.com/reference#retrieve-projects-mappings
    AttributeMapping and AttributeMappingCollection do not inherit from BaseResource and BaseCollection.
    BC and BR require a specific URL for each individual attribute mapping
    (ex: /projects/1/attributeMappings/1), but these types of URLs do not exist for attribute mappings
    """

    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        """:type: str"""
        return self._data["id"]

    @property
    def relative_id(self):
        """:type: str"""
        return self._data["relativeId"]

    @property
    def input_attribute_id(self):
        """:type: str"""
        return self._data["inputAttributeId"]

    @property
    def relative_input_attribute_id(self):
        """:type: str"""
        return self._data["relativeInputAttributeId"]

    @property
    def input_dataset_name(self):
        """:type: str"""
        return self._data["inputDatasetName"]

    @property
    def input_attribute_name(self):
        """:type: str"""
        return self._data["inputAttributeName"]

    @property
    def unified_attribute_id(self):
        """:type: str"""
        return self._data["unifiedAttributeId"]

    @property
    def relative_unified_attribute_id(self):
        """:type: str"""
        return self._data["relativeUnifiedAttributeId"]

    @property
    def unified_dataset_name(self):
        """:type: str"""
        return self._data["unifiedDatasetName"]

    @property
    def unified_attribute_name(self):
        """:type: str"""
        return self._data["unifiedAttributeName"]

    @property
    def resource_id(self):
        """:type: str"""
        spliced = self.relative_id.split("attributeMappings/")[1]
        return spliced

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

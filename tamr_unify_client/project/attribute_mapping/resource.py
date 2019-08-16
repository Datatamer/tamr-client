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


class AttributeMappingSpec:
    def __init__(self, client, data, api_path):
        self.client = client
        self._data = data
        self.api_path = api_path

    def from_data(self, data):
        return AttributeMappingSpec(self.client, data, self.api_path)

    def with_input_attribute_id(self, new_input_attribute_id):
        """:type: str"""
        return self.from_data(
            {**self._data, "inputAttributeId": new_input_attribute_id}
        )

    def with_relative_input_attribute_id(self, new_relative_input_attribute_id):
        """:type: str"""
        return self.from_data(
            {**self._data, "relativeInputAttributeId": new_relative_input_attribute_id}
        )

    def with_input_dataset_name(self, new_input_dataset_name):
        """:type: str"""
        return self.from_data(
            {**self._data, "inputDatasetName": new_input_dataset_name}
        )

    def with_input_attribute_name(self, new_input_attribute_name):
        """:type: str"""
        return self.from_data(
            {**self._data, "inputAttributeName": new_input_attribute_name}
        )

    def with_unified_attribute_id(self, new_unified_attribute_id):
        """:type: str"""
        return self.from_data(
            {**self._data, "unifiedAttributeId": new_unified_attribute_id}
        )

    def with_relative_unified_attribute_id(self, new_relative_unified_attribute_id):
        """:type: str"""
        return self.from_data(
            {
                **self._data,
                "relativeUnifiedAttributeId": new_relative_unified_attribute_id,
            }
        )

    def with_unified_dataset_name(self, new_unified_dataset_name):
        """:type: str"""
        return self.from_data(
            {**self._data, "unifiedDatasetName": new_unified_dataset_name}
        )

    def with_unified_attribute_name(self, new_unified_attribute_name):
        """:type: str"""
        return self.from_data(
            {**self._data, "unifiedAttributeName": new_unified_attribute_name}
        )

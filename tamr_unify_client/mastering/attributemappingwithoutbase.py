class AttributeMappingNoBase:
    """
       see https://docs.tamr.com/reference#retrieve-projects-mappings
       """

    def id(self, data):
        """:type: str"""
        return data["id"]

    def relative_id(self, data):
        """:type: str"""
        return data["relativeId"]

    def input_attribute_id(self, data):
        """:type: str"""
        return data["inputAttributeId"]

    def relative_input_attribute_id(self, data):
        """:type: str"""
        return data["relativeInputAttributeId"]

    def input_dataset_name(self, data):
        """:type: str"""
        return data["inputDatasetName"]

    def input_attribute_name(self, data):
        """:type: str"""
        return data["inputAttributeName"]

    def unified_attribute_id(self, data):
        """:type: str"""
        return data["unifiedAttributeId"]

    def relative_unified_attribute_id(self, data):
        """:type: str"""
        return data["relativeUnifiedAttributeId"]

    def unified_dataset_name(self, data):
        """:type: str"""
        return data["unifiedDatasetName"]

    def unified_attribute_name(self, data):
        """:type: str"""
        return data["unifiedAttributeName"]

    # def __repr__(self):
    #     return (
    #         f"{self.__class__.__module__}."
    #         f"{self.__class__.__qualname__}("
    #         f"id={self.id!r}, "
    #         f"relative_id={self.relative_id!r}, "
    #         f"input_attribute_id={self.input_attribute_id!r}, "
    #         f"relative_input_attribute_id={self.relative_input_attribute_id!r}, "
    #         f"input_dataset_name={self.input_dataset_name!r}, "
    #         f"input_attribute_name={self.input_attribute_name!r}, "
    #         f"unified_attribute_id={self.unified_attribute_id!r}, "
    #         f"relative_unified_attribute_id={self.relative_unified_attribute_id!r}, "
    #         f"unified_dataset_name={self.unified_dataset_name!r}, "
    #         f"unified_attribute_name={self.unified_attribute_name!r})"
    #     )

import requests
from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
import json


class AttributeMappingNoBase:
    """
       see https://docs.tamr.com/reference#retrieve-projects-mappings
       """

    def __init__(self, map_url):
        self.map_url = map_url
        self.all_maps = requests.get(self.map_url).json()
        self.map_list = []
        x = 0
        for mapping in self.all_maps:
            self.map_list.append(self.all_maps[x])
            x += 1
        # length = len(self.all_maps)
        # for y in range(length):
        #     #print(self.map_list[y]["unifiedAttributeName"])
        #     print(self.all_maps[y]["unifiedAttributeName"])

    def id(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["id"]

    def relative_id(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["relativeId"]

    def input_attribute_id(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["inputAttributeId"]

    def relative_input_attribute_id(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["relativeInputAttributeId"]

    def input_dataset_name(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["inputDatasetName"]

    def input_attribute_name(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["inputAttributeName"]

    def unified_attribute_id(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["unifiedAttributeId"]

    def relative_unified_attribute_id(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["relativeUnifiedAttributeId"]

    def unified_dataset_name(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["unifiedDatasetName"]

    def unified_attribute_name(self, resource_id):
        """:type: str"""
        return self.all_maps[resource_id - 1]["unifiedAttributeName"]

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

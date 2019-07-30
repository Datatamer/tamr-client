import requests

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.attributemappingwithoutbase import (
    AttributeMappingNoBase,
)


class AttributeMappingCollectionNoBase(AttributeMappingNoBase):
    def __init__(self, map_url):
        self.map_url = map_url
        self.all_maps = requests.get(self.map_url).json()
        self.map_list = []
        x = 0
        for mapping in self.all_maps:
            self.map_list.append(self.all_maps[x])
        x += 1

    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def by_resource_id(self, resource_id):
        resource_id -= 1
        # we subtract one because the list starts with 0, but the resource id's online start with 1
        return self.map_list[resource_id]

    def by_relative_id(self, relative_id):
        length = len(self.all_maps)
        for y in range(length):
            print(relative_id)
            print(self.all_maps[y])
            if relative_id in str(self.all_maps[y]):
                return self.all_maps[y]

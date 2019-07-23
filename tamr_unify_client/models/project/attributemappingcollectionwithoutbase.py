from abc import abstractmethod
from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
import requests
from tamr_unify_client.models.project.attributemappingwithoutbase import (
    AttributeMappingNoBase,
)


class AttributeMappingCollectionNoBase(AttributeMappingNoBase):
    # def __init__(self, map_url):
    #     self.map_url = map_url

    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def by_resource_id(self, resource_id):
        resource_id -= 1
        # print(self.map_list[resource_id])
        # we subtract one because the list starts with 0, but the resource id's online start with 1
        # print(self.map_url)
        return AttributeMappingNoBase(self.map_url)[resource_id]

    def by_relative_id(self, relative_id):
        print("hello")

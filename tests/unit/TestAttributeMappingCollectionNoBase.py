from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.attributemappingcollectionwithoutbase import (
    AttributeMappingCollectionNoBase,
)


class TestAttributeMappingCollectionNoBase(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_by_resource_id(self):
        url = "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings"
        responses.add(responses.GET, url, json=self.mappings_json)
        tester = AttributeMappingCollectionNoBase(url)
        by_resource = tester.by_resource_id(3)
        print("resource")
        print(by_resource)
        print("rel")
        print(tester.relative_id(by_resource))

    @responses.activate
    def test_by_relative_id(self):
        url = "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings"
        responses.add(responses.GET, url, json=self.mappings_json)
        tester = AttributeMappingCollectionNoBase(url)
        by_relative = tester.by_relative_id("projects/4/attributeMappings/19629-12")
        print("relative")
        print(by_relative)
        print("relId")
        print(tester.relative_id(by_relative))

    mappings_json = [
        {
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19629-12",
            "relativeId": "projects/4/attributeMappings/19629-12",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/surname",
            "relativeInputAttributeId": "datasets/6/attributes/surname",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "surname",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/surname",
            "relativeUnifiedAttributeId": "datasets/79/attributes/surname",
            "unifiedDatasetName": "Charlotte_unified_dataset",
            "unifiedAttributeName": "surname",
        },
        {
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19629-17",
            "relativeId": "projects/4/attributeMappings/19629-17",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/address_1",
            "relativeInputAttributeId": "datasets/6/attributes/address_1",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "address_1",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/surname",
            "relativeUnifiedAttributeId": "datasets/79/attributes/surname",
            "unifiedDatasetName": "Charlotte_unified_dataset",
            "unifiedAttributeName": "surname",
        },
        {
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19630-16",
            "relativeId": "projects/4/attributeMappings/19630-16",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/street_number",
            "relativeInputAttributeId": "datasets/6/attributes/street_number",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "street_number",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/street_number",
            "relativeUnifiedAttributeId": "datasets/79/attributes/street_number",
            "unifiedDatasetName": "Charlotte_unified_dataset",
            "unifiedAttributeName": "street_number",
        },
        {
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19631-17",
            "relativeId": "projects/4/attributeMappings/19631-17",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/address_1",
            "relativeInputAttributeId": "datasets/6/attributes/address_1",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "address_1",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/address_1",
            "relativeUnifiedAttributeId": "datasets/79/attributes/address_1",
            "unifiedDatasetName": "Charlotte_unified_dataset",
            "unifiedAttributeName": "address_1",
        },
        {
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19632-9",
            "relativeId": "projects/4/attributeMappings/19632-9",
            "inputAttributeId": "unify://unified-data/v1/datasets/6/attributes/date_of_birth",
            "relativeInputAttributeId": "datasets/6/attributes/date_of_birth",
            "inputDatasetName": "febrl_sample_2k.csv",
            "inputAttributeName": "date_of_birth",
            "unifiedAttributeId": "unify://unified-data/v1/datasets/79/attributes/Birthday",
            "relativeUnifiedAttributeId": "datasets/79/attributes/Birthday",
            "unifiedDatasetName": "Charlotte_unified_dataset",
            "unifiedAttributeName": "Birthday",
        },
    ]

from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.project.attribute_mapping_collection import (
    AttributeMappingCollection,
)


class TestAttributeMappingCollection(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_by_relative_id(self):
        am_url = f"http://localhost:9100/api/versioned/v1/projects/4/attributeMappings/19054-12"
        alias = "projects/4/attributeMappings/19054-12"
        am_test = AttributeMappingCollection(self.unify, alias)
        expected = self.amc_json[0]["relativeId"]
        responses.add(responses.GET, am_url, json=self.amc_json[0])
        self.assertEqual(
            expected,
            am_test.by_relative_id("projects/4/attributeMappings/19054-12").relative_id,
        )
        print(am_test.by_relative_id("projects/4/attributeMappings/19054-12"))

    @responses.activate
    def test_stream(self):
        ac_url = f"http://localhost:9100/api/versioned/v1/projects/4/attributeMappings/"
        alias = "projects/4/attributeMappings/"
        ac_test = AttributeMappingCollection(self.unify, alias)
        responses.add(responses.GET, ac_url, json=self.amc_json)
        streamer = ac_test.stream()
        stream_content = []
        for char in streamer:
            stream_content.append(char._data)
        self.assertEqual(self.amc_json, stream_content)

    @responses.activate
    def test_create(self):
        url = f"http://localhost:9100/api/versioned/v1/projects/4/attributeMappings/"
        project_url = f"http://localhost:9100/api/versioned/v1/projects/4"
        responses.add(responses.GET, project_url, json=self.project_json)
        responses.add(responses.POST, url, json=self.create_json, status=204)
        responses.add(responses.GET, url, json=self.create_json)

        attributemapping = self.unify.projects.by_resource_id("4").attribute_mappings()
        create = attributemapping.create(self.create_json)

        self.assertEqual(create.relative_id, self.create_json["relativeId"])

    create_json = {
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
    }

    project_json = {
        "id": "unify://unified-data/v1/projects/4",
        "name": "Charlotte",
        "description": "Mastering Project",
        "type": "DEDUP",
        "unifiedDatasetName": "Charlotte_unified_dataset",
        "created": {
            "username": "admin",
            "time": "2019-06-25T20:26:50.708Z",
            "version": "3160",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-06-25T20:26:50.760Z",
            "version": "3161",
        },
        "relativeId": "projects/4",
        "externalId": "0a7b32ef-150a-4749-9f5a-1410f1a33438",
    }

    amc_json = [
        {
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19054-12",
            "relativeId": "projects/4/attributeMappings/19054-12",
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
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19055-16",
            "relativeId": "projects/4/attributeMappings/19055-16",
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
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19056-17",
            "relativeId": "projects/4/attributeMappings/19056-17",
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
            "id": "unify://unified-data/v1/projects/4/attributeMappings/19057-9",
            "relativeId": "projects/4/attributeMappings/19057-9",
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

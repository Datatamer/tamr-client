from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.attribute_mapping.resource import AttributeMapping


class TestAttributeMapping(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def test_resource(self):
        test = AttributeMapping(self.unify, self.mappings_json)

        expected = self.mappings_json["relativeId"]
        self.assertEqual(expected, test.relative_id)

        expected = self.mappings_json["id"]
        self.assertEqual(expected, test.id)

        expected = self.mappings_json["inputAttributeId"]
        self.assertEqual(expected, test.input_attribute_id)

        expected = self.mappings_json["relativeInputAttributeId"]
        self.assertEqual(expected, test.relative_input_attribute_id)

        expected = self.mappings_json["inputDatasetName"]
        self.assertEqual(expected, test.input_dataset_name)

        expected = self.mappings_json["inputAttributeName"]
        self.assertEqual(expected, test.input_attribute_name)

        expected = self.mappings_json["unifiedAttributeId"]
        self.assertEqual(expected, test.unified_attribute_id)

        expected = self.mappings_json["relativeUnifiedAttributeId"]
        self.assertEqual(expected, test.relative_unified_attribute_id)

        expected = self.mappings_json["unifiedDatasetName"]
        self.assertEqual(expected, test.unified_dataset_name)

        expected = self.mappings_json["unifiedAttributeName"]
        self.assertEqual(expected, test.unified_attribute_name)

    @responses.activate
    def test_delete(self):
        specific_url = "http://localhost:9100/api/versioned/v1/projects/4/attributeMappings/19629-12"
        responses.add(responses.DELETE, specific_url, status=204)
        delete_map = AttributeMapping(self.unify, self.mappings_json)
        final_response = delete_map.delete()
        self.assertEqual(final_response.status_code, 204)

    mappings_json = {
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
    }

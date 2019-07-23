from unittest import TestCase

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.project.attribute_mapping import AttributeMapping


class TestAttributeMapping(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def test_resource(self):
        alias = "projects/4/attributeMappings/19054-12"
        test = AttributeMapping(self.unify, self.mapping_json[0], alias)

        expected = alias
        self.assertEqual(expected, test.relative_id)

        expected = self.mapping_json[0]["id"]
        self.assertEqual(expected, test.id)

        expected = self.mapping_json[0]["inputAttributeId"]
        self.assertEqual(expected, test.input_attribute_id)

        expected = self.mapping_json[0]["relativeInputAttributeId"]
        self.assertEqual(expected, test.relative_input_attribute_id)

        expected = self.mapping_json[0]["inputDatasetName"]
        self.assertEqual(expected, test.input_dataset_name)

        expected = self.mapping_json[0]["inputAttributeName"]
        self.assertEqual(expected, test.input_attribute_name)

        expected = self.mapping_json[0]["unifiedAttributeId"]
        self.assertEqual(expected, test.unified_attribute_id)

        expected = self.mapping_json[0]["relativeUnifiedAttributeId"]
        self.assertEqual(expected, test.relative_unified_attribute_id)

        expected = self.mapping_json[0]["unifiedDatasetName"]
        self.assertEqual(expected, test.unified_dataset_name)

        expected = self.mapping_json[0]["unifiedAttributeName"]
        self.assertEqual(expected, test.unified_attribute_name)

    def test_resource_from_json(self):
        alias = "projects/4/attributeMappings/19054-12"
        expected = AttributeMapping(self.unify, self.mapping_json[0], alias)
        actual = AttributeMapping.from_json(self.unify, self.mapping_json[0], alias)
        self.assertEqual(repr(expected), repr(actual))

    mapping_json = [
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
        }
    ]

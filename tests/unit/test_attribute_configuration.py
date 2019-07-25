from unittest import TestCase

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.attribute_configuration.resource import (
    AttributeConfiguration,
)


class TestAttributeConfiguration(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def test_resource(self):
        alias = "projects/1/attributeConfigurations/26"
        test = AttributeConfiguration(self.unify, self.ac_json, alias)

        expected = alias
        self.assertEqual(expected, test.relative_id)

        expected = self.ac_json["id"]
        self.assertEqual(expected, test.id)

        expected = self.ac_json["relativeAttributeId"]
        self.assertEqual(expected, test.relative_attribute_id)

        expected = self.ac_json["attributeRole"]
        self.assertEqual(expected, test.attribute_role)

        expected = self.ac_json["similarityFunction"]
        self.assertEqual(expected, test.similarity_function)

        expected = self.ac_json["enabledForMl"]
        self.assertEqual(expected, test.enabled_for_ml)

        expected = self.ac_json["tokenizer"]
        self.assertEqual(expected, test.tokenizer)

        expected = self.ac_json["numericFieldResolution"]
        self.assertEqual(expected, test.numeric_field_resolution)

        expected = self.ac_json["attributeName"]
        self.assertEqual(expected, test.attribute_name)

    def test_resource_from_json(self):
        alias = "projects/1/attributeConfigurations/26"
        expected = AttributeConfiguration(self.unify, self.ac_json, alias)
        actual = AttributeConfiguration.from_json(self.unify, self.ac_json, alias)
        self.assertEqual(repr(expected), repr(actual))

    ac_json = {
        "id": "unify://unified-data/v1/projects/1/attributeConfigurations/26",
        "relativeId": "projects/1/attributeConfigurations/26",
        "relativeAttributeId": "datasets/8/attributes/surname",
        "attributeRole": "CLUSTER_NAME_ATTRIBUTE",
        "similarityFunction": "COSINE",
        "enabledForMl": True,
        "tokenizer": "DEFAULT",
        "numericFieldResolution": [],
        "attributeName": "surname",
    }

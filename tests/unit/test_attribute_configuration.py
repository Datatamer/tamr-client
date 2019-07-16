from unittest import TestCase

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.attribute_configuration.resource import (
    AttributeConfiguration,
)


class TestAttributeConfiguration(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def test_resource(self):
        alias = "projects/1/attributeConfigurations/26"
        test = AttributeConfiguration(self.unify, self.AC_json[0], alias)

        expected = alias
        self.assertEqual(expected, test.relative_id)

        expected = self.AC_json[0]["id"]
        self.assertEqual(expected, test.id)

        expected = self.AC_json[0]["relativeAttributeId"]
        self.assertEqual(expected, test.relative_attribute_id)

        expected = self.AC_json[0]["attributeRole"]
        self.assertEqual(expected, test.attribute_role)

        expected = self.AC_json[0]["similarityFunction"]
        self.assertEqual(expected, test.similarity_function)

        expected = self.AC_json[0]["enabledForMl"]
        self.assertEqual(expected, test.enabled_for_ml)

        expected = self.AC_json[0]["tokenizer"]
        self.assertEqual(expected, test.tokenizer)

        expected = self.AC_json[0]["numericFieldResolution"]
        self.assertEqual(expected, test.numeric_field_resolution)

        expected = self.AC_json[0]["attributeName"]
        self.assertEqual(expected, test.attribute_name)

    def test_resource_from_json(self):
        alias = "projects/1/attributeConfigurations/26"
        expected = AttributeConfiguration(self.unify, self.AC_json[0], alias)
        actual = AttributeConfiguration.from_json(self.unify, self.AC_json[0], alias)
        self.assertEqual(repr(expected), repr(actual))

    AC_json = [
        {
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
    ]

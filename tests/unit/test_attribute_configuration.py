from unittest import TestCase

from requests import HTTPError
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.attribute_configuration.collection import (
    AttributeConfigurationCollection,
)
from tamr_unify_client.project.attribute_configuration.resource import (
    AttributeConfiguration,
)


class TestAttributeConfiguration(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.tamr = Client(auth)

    def test_resource(self):
        alias = "projects/1/attributeConfigurations/26"
        test = AttributeConfiguration(self.tamr, self._ac_json, alias)

        expected = alias
        self.assertEqual(expected, test.relative_id)

        expected = self._ac_json["id"]
        self.assertEqual(expected, test.id)

        expected = self._ac_json["relativeAttributeId"]
        self.assertEqual(expected, test.relative_attribute_id)

        expected = self._ac_json["attributeRole"]
        self.assertEqual(expected, test.attribute_role)

        expected = self._ac_json["similarityFunction"]
        self.assertEqual(expected, test.similarity_function)

        expected = self._ac_json["enabledForMl"]
        self.assertEqual(expected, test.enabled_for_ml)

        expected = self._ac_json["tokenizer"]
        self.assertEqual(expected, test.tokenizer)

        expected = self._ac_json["numericFieldResolution"]
        self.assertEqual(expected, test.numeric_field_resolution)

        expected = self._ac_json["attributeName"]
        self.assertEqual(expected, test.attribute_name)

    def test_resource_from_json(self):
        alias = "projects/1/attributeConfigurations/26"
        expected = AttributeConfiguration(self.tamr, self._ac_json, alias)
        actual = AttributeConfiguration.from_json(self.tamr, self._ac_json, alias)
        self.assertEqual(repr(expected), repr(actual))

    @responses.activate
    def test_delete(self):
        base = "http://localhost:9100/api/versioned/v1"
        alias = "projects/1/attributeConfigurations"
        attribute_id = "26"

        url = f"{base}/{alias}/{attribute_id}"
        responses.add(responses.GET, url, json=self._ac_json)
        responses.add(responses.DELETE, url, status=204)
        responses.add(responses.GET, url, status=404)

        collection = AttributeConfigurationCollection(self.tamr, alias)
        config = collection.by_resource_id(attribute_id)
        self.assertEqual(config._data, self._ac_json)

        response = config.delete()
        self.assertEqual(response.status_code, 204)
        self.assertRaises(HTTPError, lambda: collection.by_resource_id(attribute_id))

    _ac_json = {
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

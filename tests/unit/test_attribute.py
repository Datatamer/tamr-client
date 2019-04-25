from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.attribute.resource import Attribute


class TestAttribute(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def test_resource(self):
        alias = "datasets/1/attributes/RowNum"
        row_num = Attribute(self.unify, self._attributes_json[0], alias)

        expected = alias
        self.assertEqual(expected, row_num.relative_id)

        expected = self._attributes_json[0]["name"]
        self.assertEqual(expected, row_num.name)

        expected = self._attributes_json[0]["description"]
        self.assertEqual(expected, row_num.description)

        expected = self._attributes_json[0]["isNullable"]
        self.assertEqual(expected, row_num.is_nullable)

    def test_resource_from_json(self):
        alias = "datasets/1/attributes/RowNum"
        expected = Attribute(self.unify, self._attributes_json[0], alias)
        actual = Attribute.from_json(self.unify, self._attributes_json[0], alias)
        self.assertEqual(repr(expected), repr(actual))

    def test_simple_type(self):
        alias = "datasets/1/attributes/RowNum"
        row_num = Attribute(self.unify, self._attributes_json[0], alias)
        row_num_type = row_num.type
        expected = self._attributes_json[0]["type"]["baseType"]
        self.assertEqual(expected, row_num_type.base_type)
        self.assertIsNone(row_num_type.inner_type)
        self.assertSequenceEqual([], list(row_num_type.attributes))

    def test_complex_type(self):
        alias = "datasets/1/attributes/geom"
        geom = Attribute(self.unify, self._attributes_json[1], alias)
        self.assertEqual('RECORD', geom.type.base_type)
        self.assertIsNone(geom.type.inner_type)
        self.assertEqual(3, len(list(geom.type.attributes)))

        point = list(geom.type.attributes)[0]
        self.assertEqual('point', point.name)
        self.assertEqual(alias + "/type/attributes/point", point.relative_id)
        self.assertTrue(point.is_nullable)
        self.assertEqual('ARRAY', point.type.base_type)
        self.assertEqual('DOUBLE', point.type.inner_type.base_type)
        self.assertSequenceEqual([], list(point.type.attributes))

    @responses.activate
    def test_dataset_attributes(self):
        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        attributes_url = f"http://localhost:9100/api/versioned/v1/datasets/1/attributes"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)
        responses.add(responses.GET, attributes_url, json=self._attributes_json)
        dataset = self.unify.datasets.by_resource_id("1")
        print(dataset._data)
        self.assertSequenceEqual(
            self._dataset_json["keyAttributeNames"],
            dataset.key_attribute_names
        )
        attributes = list(dataset.attributes)
        self.assertEqual(2, len(attributes))
        alias = "datasets/1/attributes/RowNum"
        self.assertEqual(alias, attributes[0].relative_id)

    _dataset_json = {
        "id": "unify://unified-data/v1/datasets/1",
        "externalId": "number 1",
        "name": "dataset 1 name",
        "description": "dataset 1 description",
        "version": "dataset 1 version",
        "keyAttributeNames": ["tamr_id"],
        "tags": [],
        "created": {
            "username": "admin",
            "time": "2018-09-10T16:06:20.636Z",
            "version": "dataset 1 created version",
        },
        "lastModified": {
            "username": "admin",
            "time": "2018-09-10T16:06:20.851Z",
            "version": "dataset 1 modified version",
        },
        "relativeId": "datasets/1",
        "upstreamDatasetIds": [],
    }

    _attributes_json = [
        {
            "name": "RowNum",
            "description": "Synthetic row number",
            "type": {
                "baseType": "STRING",
                "attributes": []
            },
            "isNullable": False
        },
        {
            "name": "geom",
            "description": "",
            "type": {
                "baseType": "RECORD",
                "attributes": [
                    {
                        "name": "point",
                        "type": {
                            "baseType": "ARRAY",
                            "innerType": {
                                "baseType": "DOUBLE",
                                "attributes": []
                            },
                            "attributes": []
                        },
                        "isNullable": True
                    },
                    {
                        "name": "lineString",
                        "type": {
                            "baseType": "ARRAY",
                            "innerType": {
                                "baseType": "ARRAY",
                                "innerType": {
                                    "baseType": "DOUBLE",
                                    "attributes": []
                                },
                                "attributes": []
                            },
                            "attributes": []
                        },
                        "isNullable": True
                    },
                    {
                        "name": "polygon",
                        "type": {
                            "baseType": "ARRAY",
                            "innerType": {
                                "baseType": "ARRAY",
                                "innerType": {
                                    "baseType": "ARRAY",
                                    "innerType": {
                                        "baseType": "DOUBLE",
                                        "attributes": []
                                    },
                                    "attributes": []
                                },
                                "attributes": []
                            },
                            "attributes": []
                        },
                        "isNullable": True
                    }
                ]
            },
            "isNullable": False
        }
    ]

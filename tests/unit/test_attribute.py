from functools import partial
import json
from unittest import TestCase

from requests import HTTPError
import responses

from tamr_unify_client import Client
from tamr_unify_client.attribute.collection import AttributeCollection
from tamr_unify_client.attribute.resource import Attribute, AttributeSpec
from tamr_unify_client.attribute.type import AttributeTypeSpec
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.dataset.resource import Dataset


class TestAttribute(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.tamr = Client(auth)

    def test_resource(self):
        alias = "datasets/1/attributes/RowNum"
        row_num = Attribute(self.tamr, self._attributes_json[0], alias)

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
        expected = Attribute(self.tamr, self._attributes_json[0], alias)
        actual = Attribute.from_json(self.tamr, self._attributes_json[0], alias)
        self.assertEqual(repr(expected), repr(actual))

    def test_simple_type(self):
        alias = "datasets/1/attributes/RowNum"
        row_num = Attribute(self.tamr, self._attributes_json[0], alias)
        row_num_type = row_num.type
        expected = self._attributes_json[0]["type"]["baseType"]
        self.assertEqual(expected, row_num_type.base_type)
        self.assertIsNone(row_num_type.inner_type)
        self.assertSequenceEqual([], list(row_num_type.attributes))

    def test_complex_type(self):
        alias = "datasets/1/attributes/geom"
        geom = Attribute(self.tamr, self._attributes_json[1], alias)
        self.assertEqual("RECORD", geom.type.base_type)
        self.assertIsNone(geom.type.inner_type)
        self.assertEqual(3, len(list(geom.type.attributes)))

        point = geom.type.attributes[0]
        self.assertEqual("point", point.name)
        self.assertTrue(point.is_nullable)
        self.assertEqual("ARRAY", point.type.base_type)
        self.assertEqual("DOUBLE", point.type.inner_type.base_type)
        self.assertSequenceEqual([], list(point.type.attributes))

    @responses.activate
    def test_dataset_attributes(self):
        dataset_url = "http://localhost:9100/api/versioned/v1/datasets/1"
        attributes_url = "http://localhost:9100/api/versioned/v1/datasets/1/attributes"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)
        responses.add(responses.GET, attributes_url, json=self._attributes_json)
        dataset = self.tamr.datasets.by_resource_id("1")
        self.assertSequenceEqual(
            self._dataset_json["keyAttributeNames"], dataset.key_attribute_names
        )
        attributes = list(dataset.attributes)
        self.assertEqual(2, len(attributes))
        alias = "datasets/1/attributes/RowNum"
        self.assertEqual(alias, attributes[0].relative_id)

    @responses.activate
    def test_delete_attribute(self):
        url = "http://localhost:9100/api/versioned/v1/datasets/1/attributes/RowNum"
        responses.add(responses.GET, url, json=self._attributes_json[0])
        responses.add(responses.DELETE, url, status=204)
        responses.add(responses.GET, url, status=404)

        dataset = Dataset(self.tamr, self._dataset_json)
        attribute = dataset.attributes.by_resource_id("RowNum")
        self.assertEqual(attribute._data, self._attributes_json[0])

        response = attribute.delete()
        self.assertEqual(response.status_code, 204)
        self.assertRaises(
            HTTPError, lambda: dataset.attributes.by_resource_id("RowNum")
        )

    @responses.activate
    def test_update_attribute(self):
        def create_callback(request, snoop):
            snoop["payload"] = request.body
            return 200, {}, json.dumps(self._updated_attribute_json)

        relative_id = "dataset/1/attributes/RowNum"
        attribute_url = f"http://localhost:9100/api/versioned/v1/{relative_id}"
        snoop_dict = {}
        responses.add_callback(
            responses.PUT, attribute_url, partial(create_callback, snoop=snoop_dict)
        )
        attribute = Attribute(self.tamr, self._attributes_json[0], relative_id)

        temp_spec = attribute.spec()
        new_attribute = temp_spec.with_description(
            self._updated_attribute_json["description"]
        ).put()
        self.assertEqual(new_attribute.name, self._updated_attribute_json["name"])
        self.assertEqual(
            new_attribute.description, self._updated_attribute_json["description"]
        )

        self.assertEqual(
            json.loads(snoop_dict["payload"]), self._updated_attribute_json
        )

        self.assertEqual(attribute.name, self._attributes_json[0]["name"])
        self.assertEqual(attribute.description, self._attributes_json[0]["description"])

        # checking that intermediate didn't change
        self.assertEqual(
            temp_spec.to_dict()["description"], self._attributes_json[0]["description"]
        )

    @responses.activate
    def test_create_from_spec(self):
        def create_callback(request, snoop):
            snoop["payload"] = json.loads(request.body)
            return 201, {}, json.dumps(spec_json)

        spec_json = {
            "name": "attr",
            "isNullable": False,
            "type": {
                "baseType": "RECORD",
                "attributes": [
                    {
                        "name": str(i),
                        "isNullable": True,
                        "type": {
                            "baseType": "ARRAY",
                            "innerType": {"baseType": "STRING"},
                        },
                    }
                    for i in range(4)
                ],
            },
        }

        inner_spec = (
            AttributeSpec.new()
            .with_type(
                AttributeTypeSpec.new()
                .with_base_type("ARRAY")
                .with_inner_type(AttributeTypeSpec.new().with_base_type("STRING"))
            )
            .with_is_nullable(True)
        )
        attr_specs = [inner_spec.with_name(str(i)) for i in range(4)]
        outer_spec = (
            AttributeTypeSpec.new().with_base_type("RECORD").with_attributes(attr_specs)
        )
        spec = (
            AttributeSpec.new()
            .with_name("attr")
            .with_is_nullable(False)
            .with_type(outer_spec)
        )

        snoop_dict = {}
        rel_path = "projects/1/attributes"
        base_path = "http://localhost:9100/api/versioned/v1"
        responses.add_callback(
            responses.POST,
            f"{base_path}/{rel_path}",
            partial(create_callback, snoop=snoop_dict),
        )

        collection = AttributeCollection(self.tamr, rel_path)
        collection.create(spec.to_dict())

        self.assertEqual(snoop_dict["payload"], spec_json)

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
            "type": {"baseType": "STRING", "attributes": []},
            "isNullable": False,
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
                            "innerType": {"baseType": "DOUBLE", "attributes": []},
                            "attributes": [],
                        },
                        "isNullable": True,
                    },
                    {
                        "name": "lineString",
                        "type": {
                            "baseType": "ARRAY",
                            "innerType": {
                                "baseType": "ARRAY",
                                "innerType": {"baseType": "DOUBLE", "attributes": []},
                                "attributes": [],
                            },
                            "attributes": [],
                        },
                        "isNullable": True,
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
                                        "attributes": [],
                                    },
                                    "attributes": [],
                                },
                                "attributes": [],
                            },
                            "attributes": [],
                        },
                        "isNullable": True,
                    },
                ],
            },
            "isNullable": False,
        },
    ]

    _updated_attribute_json = {
        "name": "RowNum",
        "description": "Synthetic row number updated",
        "type": {"baseType": "STRING", "attributes": []},
        "isNullable": False,
    }

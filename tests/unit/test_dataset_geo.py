import simplejson as json
from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.dataset.resource import Dataset


class TestDatasetGeo(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def test_record_to_feature(self):
        empty_record = {"id": "1"}

        def key_value_single(rec):
            return rec["id"]

        actual = Dataset._record_to_feature(empty_record, key_value_single, ["id"], "geom")
        expected = {"type": "Feature", "id": "1"}
        self.assertEqual(expected, actual)

        record_with_point = {"id": "1", "geom": {"point": [1, 1]}}
        actual = Dataset._record_to_feature(record_with_point, key_value_single, ["id"], "geom")
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "Point", "coordinates": [1, 1]}
        }
        self.assertEqual(expected, actual)

        record_with_multi_point = {"id": "1", "geom": {"multiPoint": [[1, 1]]}}
        actual = Dataset._record_to_feature(
            record_with_multi_point, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "MultiPoint", "coordinates": [[1, 1]]}
        }
        self.assertEqual(expected, actual)

        record_with_line = {"id": "1", "geom": {"lineString": [[1, 1], [2, 2]]}}
        actual = Dataset._record_to_feature(record_with_line, key_value_single, ["id"], "geom")
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "LineString", "coordinates": [[1, 1], [2, 2]]}
        }
        self.assertEqual(expected, actual)

        record_with_multi_line = {"id": "1", "geom": {"multiLineString": [[[1, 1], [2, 2]]]}}
        actual = Dataset._record_to_feature(
            record_with_multi_line, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "MultiLineString", "coordinates": [[[1, 1], [2, 2]]]}
        }
        self.assertEqual(expected, actual)

        record_with_polygon = {"id": "1", "geom": {"polygon": [[[1, 1], [2, 2], [3, 3]]]}}
        actual = Dataset._record_to_feature(record_with_polygon, key_value_single, ["id"], "geom")
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "Polygon", "coordinates": [[[1, 1], [2, 2], [3, 3]]]}
        }
        self.assertEqual(expected, actual)

        record_with_multi_polygon = {"id": "1",
                                     "geom": {"multiPolygon": [[[[1, 1], [2, 2], [3, 3]]]]}
                                     }
        actual = Dataset._record_to_feature(
            record_with_multi_polygon, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "MultiPolygon", "coordinates": [[[[1, 1], [2, 2], [3, 3]]]]}
        }
        self.assertEqual(expected, actual)

        record_with_full_geo = {
            "id": "1",
            "geom": {
                "point": None,
                "multiPoint": None,
                "lineString": None,
                "multiLineString": None,
                "polygon": None,
                "multiPolygon": [[[[1, 1], [2, 2], [3, 3]]]]
            }
        }
        actual = Dataset._record_to_feature(record_with_full_geo, key_value_single, ["id"], "geom")
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "MultiPolygon", "coordinates": [[[[1, 1], [2, 2], [3, 3]]]]}
        }
        self.assertEqual(expected, actual)

        record_with_null_geo = {
            "id": "1",
            "geom": {
                "point": None, "multiPoint": None,
                "lineString": None, "multiLineString": None,
                "polygon": None, "multiPolygon": None
            }
        }
        actual = Dataset._record_to_feature(record_with_null_geo, key_value_single, ["id"], "geom")
        expected = {
            "type": "Feature",
            "id": "1"
        }
        self.assertEqual(expected, actual)

        record_with_bbox = {"id": "1", "bbox": [[0, 0], [1, 1]]}
        actual = Dataset._record_to_feature(record_with_bbox, key_value_single, ["id"], "geom")
        expected = {
            "type": "Feature",
            "id": "1",
            "bbox": [[0, 0], [1, 1]]
        }
        self.assertEqual(expected, actual)

        record_with_props = {"id": "1", "p1": "v1", "p2": "v2"}
        actual = Dataset._record_to_feature(record_with_props, key_value_single, ["id"], "geom")
        expected = {
            "type": "Feature",
            "id": "1",
            "properties": {
                "p1": "v1",
                "p2": "v2"
            }
        }
        self.assertEqual(expected, actual)

        def key_value_composite(rec):
            return [rec[v] for v in ["id1", "id2"]]

        record_with_composite_key = {"id1": "1", "id2": "2"}
        actual = Dataset._record_to_feature(
            record_with_composite_key,
            key_value_composite,
            ["id1", "id2"],
            "geom"
        )
        expected = {
            "type": "Feature",
            "id": ["1", "2"]
        }
        self.assertEqual(expected, actual)

        record_with_everything = {
            "id1": "1",
            "id2": "2",
            "bbox": [[0, 0], [1, 1]],
            "name": "record with everything",
            "geom": {
                "point": None,
                "multiPoint": None,
                "lineString": None,
                "multiLineString": None,
                "polygon": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
                "multiPolygon": None
            },
            "alternate_geom": {
                "point": [1, 1],
                "multiPoint": None,
                "lineString": None,
                "multiLineString": None,
                "polygon": None,
                "multiPolygon": None
            }
        }
        actual = Dataset._record_to_feature(
            record_with_everything,
            key_value_composite,
            ["id1", "id2"],
            "geom"
        )
        expected = {
            "type": "Feature",
            "id": ["1", "2"],
            "bbox": [[0, 0], [1, 1]],
            "properties": {
                "name": "record with everything",
                "alternate_geom": {
                    "point": [1, 1],
                    "multiPoint": None,
                    "lineString": None,
                    "multiLineString": None,
                    "polygon": None,
                    "multiPolygon": None
                }
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
            },
        }
        self.assertEqual(expected, actual)

    @responses.activate
    def test_geo_features(self):
        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)

        attributes_url = f"{dataset_url}/attributes"
        responses.add(responses.GET, attributes_url, json=self._attributes_json)

        records_url = f"{dataset_url}/records"
        responses.add(responses.GET, records_url, body="\n".join(
            [json.dumps(rec) for rec in self._records_json]
        ))
        dataset = self.unify.datasets.by_resource_id("1")
        features = [feature for feature in dataset.__geo_features__]
        self.assertEqual(6, len(features))
        self.assertSetEqual(
            {
                "point", "multiPoint",
                "lineString", "multiLineString",
                "polygon", "multiPolygon"
            },
            {feature["id"] for feature in features}
        )

    @responses.activate
    def test_geo_interface(self):
        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)

        attributes_url = f"{dataset_url}/attributes"
        responses.add(responses.GET, attributes_url, json=self._attributes_json)

        records_url = f"{dataset_url}/records"
        responses.add(responses.GET, records_url, body="\n".join(
            [json.dumps(rec) for rec in self._records_json]
        ))
        dataset = self.unify.datasets.by_resource_id("1")
        fc = dataset.__geo_interface__
        self.assertEqual("FeatureCollection", fc["type"])
        self.assertSetEqual(
            {
                "point", "multiPoint",
                "lineString", "multiLineString",
                "polygon", "multiPolygon"
            },
            {feature["id"] for feature in fc["features"]}
        )

    _dataset_json = {
        "id": "unify://unified-data/v1/datasets/1",
        "externalId": "number 1",
        "name": "dataset 1 name",
        "description": "dataset 1 description",
        "version": "dataset 1 version",
        "keyAttributeNames": ["id"],
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
            "name": "id",
            "description": "primary key",
            "type": {"baseType": "STRING", "attributes": []},
            "isNullable": False,
        },
        {
            "name": "geom",
            "description": "Geospatial geometry",
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
                        "name": "multiPoint",
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
                        "name": "multiLineString",
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
                    {
                        "name": "multiPolygon",
                        "type": {
                            "baseType": "ARRAY",
                            "innerType": {
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
                            "attributes": [],
                        },
                        "isNullable": True,
                    }
                ],
            },
            "isNullable": False,
        },
    ]

    _records_json = [
        {"id": "point", "geom": {"point": [1, 1]}},
        {"id": "multiPoint", "geom": {"multiPoint": [[1, 1], [2, 2]]}},
        {"id": "lineString", "geom": {"lineString": [[1, 1], [2, 2]]}},
        {"id": "multiLineString",
         "geom": {"multiLineString": [[[1, 1], [2, 2]], [[3, 3], [4, 4]]]}},
        {"id": "polygon", "geom": {"polygon": [[[1, 1], [2, 2], [3, 3], [1, 1]]]}},
        {"id": "multiPolygon", "geom": {
            "multiPolygon": [[[[1, 1], [2, 2], [3, 3], [1, 1]]],
                             [[[4, 4], [5, 5], [6, 6], [4, 4]]]]}}
    ]

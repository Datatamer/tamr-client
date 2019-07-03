from copy import deepcopy
from functools import partial
import json
from unittest import TestCase

import pytest
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

        actual = Dataset._record_to_feature(
            empty_record, key_value_single, ["id"], "geom"
        )
        expected = {"type": "Feature", "id": "1"}
        self.assertEqual(expected, actual)

        record_with_point = {"id": "1", "geom": {"point": [1, 1]}}
        actual = Dataset._record_to_feature(
            record_with_point, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "Point", "coordinates": [1, 1]},
        }
        self.assertEqual(expected, actual)

        record_with_multi_point = {"id": "1", "geom": {"multiPoint": [[1, 1]]}}
        actual = Dataset._record_to_feature(
            record_with_multi_point, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "MultiPoint", "coordinates": [[1, 1]]},
        }
        self.assertEqual(expected, actual)

        record_with_line = {"id": "1", "geom": {"lineString": [[1, 1], [2, 2]]}}
        actual = Dataset._record_to_feature(
            record_with_line, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "LineString", "coordinates": [[1, 1], [2, 2]]},
        }
        self.assertEqual(expected, actual)

        record_with_multi_line = {
            "id": "1",
            "geom": {"multiLineString": [[[1, 1], [2, 2]]]},
        }
        actual = Dataset._record_to_feature(
            record_with_multi_line, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "MultiLineString", "coordinates": [[[1, 1], [2, 2]]]},
        }
        self.assertEqual(expected, actual)

        record_with_polygon = {
            "id": "1",
            "geom": {"polygon": [[[1, 1], [2, 2], [3, 3]]]},
        }
        actual = Dataset._record_to_feature(
            record_with_polygon, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "Polygon", "coordinates": [[[1, 1], [2, 2], [3, 3]]]},
        }
        self.assertEqual(expected, actual)

        record_with_multi_polygon = {
            "id": "1",
            "geom": {"multiPolygon": [[[[1, 1], [2, 2], [3, 3]]]]},
        }
        actual = Dataset._record_to_feature(
            record_with_multi_polygon, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[1, 1], [2, 2], [3, 3]]]],
            },
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
                "multiPolygon": [[[[1, 1], [2, 2], [3, 3]]]],
            },
        }
        actual = Dataset._record_to_feature(
            record_with_full_geo, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[1, 1], [2, 2], [3, 3]]]],
            },
        }
        self.assertEqual(expected, actual)

        record_with_null_geo = {
            "id": "1",
            "geom": {
                "point": None,
                "multiPoint": None,
                "lineString": None,
                "multiLineString": None,
                "polygon": None,
                "multiPolygon": None,
            },
        }
        actual = Dataset._record_to_feature(
            record_with_null_geo, key_value_single, ["id"], "geom"
        )
        expected = {"geometry": None, "type": "Feature", "id": "1"}
        self.assertEqual(expected, actual)

        record_with_bbox = {"id": "1", "bbox": [[0, 0], [1, 1]]}
        actual = Dataset._record_to_feature(
            record_with_bbox, key_value_single, ["id"], "geom"
        )
        expected = {"type": "Feature", "id": "1", "bbox": [[0, 0], [1, 1]]}
        self.assertEqual(expected, actual)

        record_with_props = {"id": "1", "p1": "v1", "p2": "v2"}
        actual = Dataset._record_to_feature(
            record_with_props, key_value_single, ["id"], "geom"
        )
        expected = {
            "type": "Feature",
            "id": "1",
            "properties": {"p1": "v1", "p2": "v2"},
        }
        self.assertEqual(expected, actual)

        def key_value_composite(rec):
            return [rec[v] for v in ["id1", "id2"]]

        record_with_composite_key = {"id1": "1", "id2": "2"}
        actual = Dataset._record_to_feature(
            record_with_composite_key, key_value_composite, ["id1", "id2"], "geom"
        )
        expected = {"type": "Feature", "id": ["1", "2"]}
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
                "multiPolygon": None,
            },
            "alternate_geom": {
                "point": [1, 1],
                "multiPoint": None,
                "lineString": None,
                "multiLineString": None,
                "polygon": None,
                "multiPolygon": None,
            },
        }
        actual = Dataset._record_to_feature(
            record_with_everything, key_value_composite, ["id1", "id2"], "geom"
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
                    "multiPolygon": None,
                },
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]],
            },
        }
        self.assertEqual(expected, actual)

        record_without_geo = {"id": "1", "prop1": "val1"}
        actual = Dataset._record_to_feature(
            record_without_geo, key_value_single, ["id"], None
        )
        expected = {"type": "Feature", "id": "1", "properties": {"prop1": "val1"}}
        self.assertEqual(expected, actual)

    @responses.activate
    def test_geo_features(self):
        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)

        attributes_url = f"{dataset_url}/attributes"
        responses.add(responses.GET, attributes_url, json=self._attributes_json)

        records_url = f"{dataset_url}/records"
        responses.add(
            responses.GET,
            records_url,
            body="\n".join([json.dumps(rec) for rec in self._records_json]),
        )
        dataset = self.unify.datasets.by_resource_id("1")
        features = [feature for feature in dataset.itergeofeatures()]
        self.assertEqual(6, len(features))
        self.assertSetEqual(
            {
                "point",
                "multiPoint",
                "lineString",
                "multiLineString",
                "polygon",
                "multiPolygon",
            },
            {feature["id"] for feature in features},
        )

    @responses.activate
    def test_geo_features_geo_attr(self):
        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)

        # Create a dataset with multiple geometry attributes
        multi_geo_attrs = deepcopy(self._attributes_json)
        geo2_attr = deepcopy(multi_geo_attrs[-1])
        geo2_attr["name"] = "geom2"
        multi_geo_attrs.append(geo2_attr)
        attributes_url = f"{dataset_url}/attributes"
        responses.add(responses.GET, attributes_url, json=multi_geo_attrs)

        # Create a record with multiple geometry attributes
        record = {"id": "point", "geom": {"point": [1, 1]}, "geom2": {"point": [2, 2]}}
        records_url = f"{dataset_url}/records"
        responses.add(responses.GET, records_url, body=json.dumps(record))
        dataset = self.unify.datasets.by_resource_id("1")

        # Default is to get the first attribute with geometry type
        feature = next(dataset.itergeofeatures())
        self.assertEqual(feature["geometry"]["coordinates"], record["geom"]["point"])

        # We can override which geometry attribute is used for geometry
        feature = next(dataset.itergeofeatures(geo_attr="geom2"))
        self.assertEqual(feature["geometry"]["coordinates"], record["geom2"]["point"])

    @responses.activate
    def test_geo_interface(self):
        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)

        attributes_url = f"{dataset_url}/attributes"
        responses.add(responses.GET, attributes_url, json=self._attributes_json)

        records_url = f"{dataset_url}/records"
        responses.add(
            responses.GET,
            records_url,
            body="\n".join([json.dumps(rec) for rec in self._records_json]),
        )
        dataset = self.unify.datasets.by_resource_id("1")
        fc = dataset.__geo_interface__
        self.assertEqual("FeatureCollection", fc["type"])
        self.assertSetEqual(
            {
                "point",
                "multiPoint",
                "lineString",
                "multiLineString",
                "polygon",
                "multiPolygon",
            },
            {feature["id"] for feature in fc["features"]},
        )

    def test_feature_to_record(self):
        feature = {"type": "Feature", "id": "1"}
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1"}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "Point", "coordinates": [0, 0]},
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"point": [0, 0]}}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "MultiPoint", "coordinates": [[0, 0], [1, 1]]},
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"multiPoint": [[0, 0], [1, 1]]}}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"lineString": [[0, 0], [1, 1]]}}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [[[0, 0], [1, 1], [2, 2]]],
            },
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"multiLineString": [[[0, 0], [1, 1], [2, 2]]]}}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 1], [2, 2]]]},
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"polygon": [[[0, 0], [1, 1], [2, 2]]]}}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[0, 0], [1, 1], [2, 2]]]],
            },
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"multiPolygon": [[[[0, 0], [1, 1], [2, 2]]]]}}
        self.assertEqual(expected, actual)

        feature = {"type": "Feature", "id": "1", "geometry": None}
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1"}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "bbox": [0, 0, 1, 1],
            "geometry": {"type": "Point", "coordinates": [0, 0]},
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"point": [0, 0]}, "bbox": [0, 0, 1, 1]}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "bbox": None,
            "geometry": {"type": "Point", "coordinates": [0, 0]},
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"point": [0, 0]}}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "bbox": [0, 0, 1, 1],
            "geometry": {"type": "Point", "coordinates": [0, 0]},
            "properties": {"prop1": "val1", "prop2": "val2"},
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {
            "pk": "1",
            "geo": {"point": [0, 0]},
            "bbox": [0, 0, 1, 1],
            "prop1": "val1",
            "prop2": "val2",
        }
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "bbox": [0, 0, 1, 1],
            "geometry": {"type": "Point", "coordinates": [0, 0]},
            "properties": None,
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"point": [0, 0]}, "bbox": [0, 0, 1, 1]}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": "1",
            "bbox": [0, 0, 1, 1],
            "geometry": {"type": "Point", "coordinates": [0, 0]},
            # Properties with names that conflict with
            # the props in the key or geometry
            # get ignored
            "properties": {"pk": "val1", "geo": "val2", "bbox": "val3"},
        }
        actual = Dataset._feature_to_record(feature, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"point": [0, 0]}, "bbox": [0, 0, 1, 1]}
        self.assertEqual(expected, actual)

        feature = {
            "type": "Feature",
            "id": ["1", "2"],
            "geometry": {"type": "Point", "coordinates": [0, 0]},
        }
        actual = Dataset._feature_to_record(feature, ["pk1", "pk2"], "geo")
        expected = {"pk1": "1", "pk2": "2", "geo": {"point": [0, 0]}}
        self.assertEqual(expected, actual)

        feature = {"type": "Feature", "id": "1", "geometry": None}
        Dataset._feature_to_record(feature, ["pk"], "geo")
        # feature_to_record is required to not raise an exception

        feature = {
            "type": "Feature",
            "id": None,
            "geometry": {"type": "Point", "coordinates": [0, 0]},
        }
        with pytest.raises(ValueError):
            Dataset._feature_to_record(feature, ["pk"], "geo")

        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [0, 0]},
        }
        with pytest.raises(ValueError):
            Dataset._feature_to_record(feature, ["pk"], "geo")

        class NotAFeature:
            @property
            def __geo_interface__(self):
                return {
                    "type": "Feature",
                    "id": "1",
                    "geometry": {"type": "Point", "coordinates": [0, 0]},
                }

        naf = NotAFeature()
        actual = Dataset._feature_to_record(naf, ["pk"], "geo")
        expected = {"pk": "1", "geo": {"point": [0, 0]}}
        self.assertEqual(expected, actual)

    @responses.activate
    def test_from_geo_features(self):
        def update_callback(request, snoop):
            snoop["payload"] = request.body
            return 200, {}, "{}"

        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)

        attributes_url = f"{dataset_url}/attributes"
        responses.add(responses.GET, attributes_url, json=self._attributes_json)

        records_url = f"{dataset_url}:updateRecords"
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, callback=partial(update_callback, snoop=snoop)
        )

        dataset = self.unify.datasets.by_resource_id("1")
        features = [
            {"id": "1", "geometry": {"type": "Point", "coordinates": [0, 0]}},
            {"id": "2", "geometry": {"type": "Point", "coordinates": [1, 1]}},
        ]
        dataset.from_geo_features(features)
        updates = [
            {
                "action": "CREATE",
                "recordId": "1",
                "record": {"geom": {"point": [0, 0]}, "id": "1"},
            },
            {
                "action": "CREATE",
                "recordId": "2",
                "record": {"geom": {"point": [1, 1]}, "id": "2"},
            },
        ]
        expected = updates
        actual = [json.loads(item) for item in snoop["payload"]]
        self.assertEqual(expected, actual)

        class NotAFeatureCollection:
            @property
            def __geo_interface__(self):
                return {"type": "FeatureCollection", "features": features}

        snoop["payload"] = None
        nafc = NotAFeatureCollection()
        dataset.from_geo_features(nafc)
        actual = [json.loads(item) for item in snoop["payload"]]
        self.assertEqual(expected, actual)

    @responses.activate
    def test_from_geo_features_geo_attr(self):
        def update_callback(request, snoop):
            snoop["payload"] = request.body
            return 200, {}, "{}"

        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, dataset_url, json=self._dataset_json)

        # Create a dataset with multiple geometry attributes
        multi_geo_attrs = deepcopy(self._attributes_json)
        geo2_attr = deepcopy(multi_geo_attrs[-1])
        geo2_attr["name"] = "geom2"
        multi_geo_attrs.append(geo2_attr)
        attributes_url = f"{dataset_url}/attributes"
        responses.add(responses.GET, attributes_url, json=multi_geo_attrs)

        records_url = f"{dataset_url}:updateRecords"
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, callback=partial(update_callback, snoop=snoop)
        )

        dataset = self.unify.datasets.by_resource_id("1")
        features = [{"id": "1", "geometry": {"type": "Point", "coordinates": [0, 0]}}]

        # by default, the first attribute with geometry type is used for geometry
        dataset.from_geo_features(features)
        expected = [
            {
                "action": "CREATE",
                "recordId": "1",
                "record": {"geom": {"point": [0, 0]}, "id": "1"},
            }
        ]
        actual = [json.loads(item) for item in snoop["payload"]]
        self.assertEqual(expected, actual)

        # We can override which geometry attribute is used for geometry
        snoop["payload"] = None
        dataset.from_geo_features(features, geo_attr="geom2")
        expected = [
            {
                "action": "CREATE",
                "recordId": "1",
                "record": {"geom2": {"point": [0, 0]}, "id": "1"},
            }
        ]
        actual = [json.loads(item) for item in snoop["payload"]]
        self.assertEqual(expected, actual)

    @responses.activate
    def test_from_geo_features_composite_key(self):
        def update_callback(request, snoop):
            snoop["payload"] = request.body
            return 200, {}, "{}"

        composite_key_dataset_json = deepcopy(self._dataset_json)
        composite_key_dataset_json["keyAttributeNames"] = ["id1", "id2"]
        dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, dataset_url, json=composite_key_dataset_json)

        composite_key_attributes_json = deepcopy(self._attributes_json)
        composite_key_attributes_json[0]["name"] = "id1"
        composite_key_attributes_json.insert(
            1, deepcopy(composite_key_attributes_json[0])
        )
        composite_key_attributes_json[1]["name"] = "id2"
        attributes_url = f"{dataset_url}/attributes"
        responses.add(responses.GET, attributes_url, json=composite_key_attributes_json)

        records_url = f"{dataset_url}:updateRecords"
        snoop = {}
        responses.add_callback(
            responses.POST, records_url, callback=partial(update_callback, snoop=snoop)
        )

        dataset = self.unify.datasets.by_resource_id("1")
        features = [
            {"id": ["1", "a"], "geometry": {"type": "Point", "coordinates": [0, 0]}},
            {"id": ["2", "b"], "geometry": {"type": "Point", "coordinates": [1, 1]}},
        ]
        dataset.from_geo_features(features)
        updates = [
            {
                "action": "CREATE",
                "compositeRecordId": ["1", "a"],
                "record": {"geom": {"point": [0, 0]}, "id1": "1", "id2": "a"},
            },
            {
                "action": "CREATE",
                "compositeRecordId": ["2", "b"],
                "record": {"geom": {"point": [1, 1]}, "id1": "2", "id2": "b"},
            },
        ]
        expected = updates
        actual = [json.loads(item) for item in snoop["payload"]]
        self.assertEqual(expected, actual)

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
                    },
                ],
            },
            "isNullable": False,
        },
    ]

    _records_json = [
        {"id": "point", "geom": {"point": [1, 1]}},
        {"id": "multiPoint", "geom": {"multiPoint": [[1, 1], [2, 2]]}},
        {"id": "lineString", "geom": {"lineString": [[1, 1], [2, 2]]}},
        {
            "id": "multiLineString",
            "geom": {"multiLineString": [[[1, 1], [2, 2]], [[3, 3], [4, 4]]]},
        },
        {"id": "polygon", "geom": {"polygon": [[[1, 1], [2, 2], [3, 3], [1, 1]]]}},
        {
            "id": "multiPolygon",
            "geom": {
                "multiPolygon": [
                    [[[1, 1], [2, 2], [3, 3], [1, 1]]],
                    [[[4, 4], [5, 5], [6, 6], [4, 4]]],
                ]
            },
        },
    ]

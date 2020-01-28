import json
from pathlib import Path

import tamr_unify_client as tc
from tests.utils import data_dir, load_json


def test_from_json():
    geom_json = load_json(data_dir / "attributes.json")[1]
    geom_type = tc.attribute_type.from_json(geom_json["type"])
    assert isinstance(geom_type, tc.attribute_type.Record)

    for i, subattr in enumerate(geom_type.attributes):
        assert isinstance(subattr, tc.SubAttribute)
        if i == 0:
            assert subattr.name == "point"
            assert subattr.type == tc.attribute_type.Array(tc.attribute_type.Double())
            assert subattr.is_nullable
            assert subattr.description is None
        elif i == 1:
            assert subattr.name == "lineString"
            assert subattr.type == tc.attribute_type.Array(
                tc.attribute_type.Array(tc.attribute_type.Double())
            )
            assert subattr.is_nullable
            assert subattr.description is None
        elif i == 2:
            assert subattr.name == "polygon"
            assert subattr.type == tc.attribute_type.Array(
                tc.attribute_type.Array(
                    tc.attribute_type.Array(tc.attribute_type.Double())
                )
            )
            assert subattr.is_nullable
            assert subattr.description is None


def test_json():
    attrs_json = load_json(data_dir / "attributes.json")
    for attr_json in attrs_json:
        attr_type_json = attr_json["type"]
        attr_type = tc.attribute_type.from_json(attr_type_json)
        assert attr_type == tc.attribute_type.from_json(
            tc.attribute_type.to_json(attr_type)
        )

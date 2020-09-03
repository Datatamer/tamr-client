import pytest

import tamr_client as tc
from tests.tamr_client import utils


def test_from_json():
    geom_json = utils.load_json("attributes.json")[1]
    geom_type = tc.attribute.type.from_json(geom_json["type"])
    assert isinstance(geom_type, tc.attribute.type.Record)

    for i, subattr in enumerate(geom_type.attributes):
        assert isinstance(subattr, tc.SubAttribute)
        if i == 0:
            assert subattr.name == "point"
            assert subattr.type == tc.attribute.type.Array(tc.attribute.type.DOUBLE)
            assert subattr.is_nullable
        elif i == 1:
            assert subattr.name == "lineString"
            assert subattr.type == tc.attribute.type.Array(
                tc.attribute.type.Array(tc.attribute.type.DOUBLE)
            )
            assert subattr.is_nullable
        elif i == 2:
            assert subattr.name == "polygon"
            assert subattr.type == tc.attribute.type.Array(
                tc.attribute.type.Array(
                    tc.attribute.type.Array(tc.attribute.type.DOUBLE)
                )
            )
            assert subattr.is_nullable


def test_from_json_missing_base_type():
    type_json: tc._types.JsonDict = {"attributes": []}

    with pytest.raises(ValueError):
        tc.attribute.type.from_json(type_json)


def test_from_json_unrecognized_base_type():
    type_json: tc._types.JsonDict = {"baseType": "NOT_A_TYPE", "attributes": []}

    with pytest.raises(ValueError):
        tc.attribute.type.from_json(type_json)


def test_from_json_array_missing_inner_type():
    type_json: tc._types.JsonDict = {"baseType": "ARRAY"}

    with pytest.raises(ValueError):
        tc.attribute.type.from_json(type_json)


def test_from_json_map_missing_inner_type():
    type_json: tc._types.JsonDict = {"baseType": "MAP"}

    with pytest.raises(ValueError):
        tc.attribute.type.from_json(type_json)


def test_from_json_record_missing_attributes():
    type_json: tc._types.JsonDict = {"baseType": "RECORD"}

    with pytest.raises(ValueError):
        tc.attribute.type.from_json(type_json)


def test_json():
    attrs_json = utils.load_json("attributes.json")
    for attr_json in attrs_json:
        attr_type_json = attr_json["type"]
        attr_type = tc.attribute.type.from_json(attr_type_json)
        assert attr_type == tc.attribute.type.from_json(
            tc.attribute.type.to_json(attr_type)
        )

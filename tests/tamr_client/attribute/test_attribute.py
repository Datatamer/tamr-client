from dataclasses import replace

import pytest
import responses

import tamr_client as tc
from tests.tamr_client import utils


def test_from_json():
    attrs_json = utils.load_json("attributes.json")
    dataset_id = 1
    for attr_json in attrs_json:
        attr_id = attr_json["name"]
        url = tc.URL(path=f"datasets/{dataset_id}/attributes/{attr_id}")
        attr = tc.attribute._from_json(url, attr_json)
        assert attr.name == attr_json["name"]
        assert attr.description == attr_json["description"]
        assert attr.is_nullable == attr_json["isNullable"]


def test_json():
    """original -> to_json -> from_json -> original"""
    attrs_json = utils.load_json("attributes.json")
    dataset_id = 1
    for attr_json in attrs_json:
        attr_id = attr_json["name"]
        url = tc.URL(f"datasets/{dataset_id}/attributes/{attr_id}")
        attr = tc.attribute._from_json(url, attr_json)
        assert attr == tc.attribute._from_json(url, tc.attribute.to_json(attr))


@responses.activate
def test_create():
    s = utils.session()
    dataset = utils.dataset()

    attrs = tuple(
        [
            tc.SubAttribute(
                name=str(i),
                is_nullable=True,
                type=tc.attribute.type.Array(tc.attribute.type.STRING),
            )
            for i in range(4)
        ]
    )

    attrs_url = tc.URL(path=dataset.url.path + "/attributes")
    url = replace(attrs_url, path=attrs_url.path + "/attr")
    attr_json = utils.load_json("attribute.json")
    responses.add(responses.POST, str(attrs_url), json=attr_json)
    attr = tc.attribute.create(
        s,
        dataset,
        name="attr",
        is_nullable=False,
        type=tc.attribute.type.Record(attributes=attrs),
    )

    assert attr == tc.attribute._from_json(url, attr_json)


@responses.activate
def test_update():
    s = utils.session()

    url = tc.URL(path="datasets/1/attributes/RowNum")
    attr_json = utils.load_json("attributes.json")[0]
    attr = tc.attribute._from_json(url, attr_json)

    updated_attr_json = utils.load_json("updated_attribute.json")
    responses.add(responses.PUT, str(attr.url), json=updated_attr_json)
    updated_attr = tc.attribute.update(
        s, attr, description=updated_attr_json["description"]
    )

    assert updated_attr == replace(attr, description=updated_attr_json["description"])


@responses.activate
def test_delete():
    s = utils.session()

    url = tc.URL(path="datasets/1/attributes/RowNum")
    attr_json = utils.load_json("attributes.json")[0]
    attr = tc.attribute._from_json(url, attr_json)

    responses.add(responses.DELETE, str(attr.url), status=204)
    tc.attribute.delete(s, attr)


@responses.activate
def test_from_resource_id():
    s = utils.session()
    dataset = utils.dataset()

    url = tc.URL(path=dataset.url.path + "/attributes/attr")
    attr_json = utils.load_json("attribute.json")
    responses.add(responses.GET, str(url), json=attr_json)
    attr = tc.attribute.from_resource_id(s, dataset, "attr")

    assert attr == tc.attribute._from_json(url, attr_json)


@responses.activate
def test_from_resource_id_attribute_not_found():
    s = utils.session()
    dataset = utils.dataset()

    url = replace(dataset.url, path=dataset.url.path + "/attributes/attr")

    responses.add(responses.GET, str(url), status=404)
    with pytest.raises(tc.attribute.NotFound):
        tc.attribute.from_resource_id(s, dataset, "attr")


def test_create_reserved_attribute_name():
    s = utils.session()
    dataset = utils.dataset()

    with pytest.raises(tc.attribute.ReservedName):
        tc.attribute.create(s, dataset, name="clusterId", is_nullable=False)


@responses.activate
def test_from_dataset_all():
    s = utils.session()
    dataset = utils.dataset()

    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")
    attrs_json = utils.load_json("attributes.json")
    responses.add(responses.GET, str(attrs_url), json=attrs_json, status=204)

    attrs = tc.attribute.from_dataset_all(s, dataset)

    row_num = attrs[0]
    assert row_num.name == "RowNum"
    assert row_num.type == tc.attribute.type.STRING

    geom = attrs[1]
    assert geom.name == "geom"
    assert isinstance(geom.type, tc.attribute.type.Record)


@responses.activate
def test_create_attribute_exists():
    s = utils.session()
    dataset = utils.dataset()

    url = replace(dataset.url, path=dataset.url.path + "/attributes")
    responses.add(responses.POST, str(url), status=409)
    with pytest.raises(tc.attribute.AlreadyExists):
        tc.attribute.create(s, dataset, name="attr", is_nullable=False)


@responses.activate
def test_update_attribute_not_found():
    s = utils.session()

    url = tc.URL(path="datasets/1/attributes/RowNum")
    attr_json = utils.load_json("attributes.json")[0]
    attr = tc.attribute._from_json(url, attr_json)

    responses.add(responses.PUT, str(attr.url), status=404)
    with pytest.raises(tc.attribute.NotFound):
        tc.attribute.update(s, attr)


@responses.activate
def test_delete_attribute_not_found():
    s = utils.session()

    url = tc.URL(path="datasets/1/attributes/RowNum")
    attr_json = utils.load_json("attributes.json")[0]
    attr = tc.attribute._from_json(url, attr_json)

    responses.add(responses.PUT, str(attr.url), status=404)
    with pytest.raises(tc.attribute.NotFound):
        attr = tc.attribute.update(s, attr)

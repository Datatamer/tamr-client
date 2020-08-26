import pytest

import tamr_client as tc
from tests.tamr_client import fake, utils


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


@fake.json
def test_create():
    s = fake.session()
    dataset = fake.dataset()

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

    attr = tc.attribute.create(
        s,
        dataset,
        name="attr",
        is_nullable=False,
        type=tc.attribute.type.Record(attributes=attrs),
    )

    assert attr.name == "attr"
    assert not attr.is_nullable
    assert isinstance(attr.type, tc.attribute.type.Record)
    assert attr.type.attributes == attrs


@fake.json
def test_update():
    s = fake.session()
    attr = fake.attribute()

    updated_attr = tc.attribute.update(
        s, attr, description="Synthetic row number updated"
    )

    assert updated_attr.description == "Synthetic row number updated"


@fake.json
def test_delete():
    s = fake.session()
    attr = fake.attribute()

    tc.attribute.delete(s, attr)


@fake.json
def test_by_resource_id():
    s = fake.session()
    dataset = fake.dataset()

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

    attr = tc.attribute.by_resource_id(s, dataset, "attr")

    assert attr.name == "attr"
    assert not attr.is_nullable
    assert isinstance(attr.type, tc.attribute.type.Record)
    assert attr.type.attributes == attrs


@fake.json
def test_by_resource_id_attribute_not_found():
    s = fake.session()
    dataset = fake.dataset()

    with pytest.raises(tc.attribute.NotFound):
        tc.attribute.by_resource_id(s, dataset, "attr")


def test_create_reserved_attribute_name():
    s = fake.session()
    dataset = fake.dataset()

    with pytest.raises(tc.attribute.ReservedName):
        tc.attribute.create(s, dataset, name="clusterId", is_nullable=False)


@fake.json
def test_create_attribute_exists():
    s = fake.session()
    dataset = fake.dataset()

    with pytest.raises(tc.attribute.AlreadyExists):
        tc.attribute.create(s, dataset, name="attr", is_nullable=False)


@fake.json
def test_update_attribute_not_found():
    s = fake.session()
    attr = fake.attribute()

    with pytest.raises(tc.attribute.NotFound):
        tc.attribute.update(s, attr)


@fake.json
def test_delete_attribute_not_found():
    s = fake.session()
    attr = fake.attribute()

    with pytest.raises(tc.attribute.NotFound):
        tc.attribute.delete(s, attr)

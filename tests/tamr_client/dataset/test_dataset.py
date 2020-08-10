import pytest

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_from_resource_id():
    s = fake.session()
    instance = fake.instance()

    dataset = tc.dataset.from_resource_id(s, instance, "1")
    assert dataset.name == "dataset 1 name"
    assert dataset.description == "dataset 1 description"
    assert dataset.key_attribute_names == ("tamr_id",)


@fake.json
def test_from_resource_id_dataset_not_found():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.dataset.NotFound):
        tc.dataset.from_resource_id(s, instance, "1")


@fake.json
def test_attributes():
    s = fake.session()
    dataset = fake.dataset()

    attrs = tc.dataset.attributes(s, dataset)

    row_num = attrs[0]
    assert row_num.name == "RowNum"
    assert row_num.type == tc.attribute.type.STRING

    geom = attrs[1]
    assert geom.name == "geom"
    assert isinstance(geom.type, tc.attribute.type.Record)

from dataclasses import replace

import pytest
import responses

import tamr_client as tc
from tests.tamr_client import fake, utils


@responses.activate
def test_from_resource_id():
    s = fake.session()
    instance = fake.instance()

    dataset_json = utils.load_json("dataset.json")
    url = tc.URL(path="datasets/1")
    responses.add(responses.GET, str(url), json=dataset_json)

    dataset = tc.dataset.from_resource_id(s, instance, "1")
    assert dataset.name == "dataset 1 name"
    assert dataset.description == "dataset 1 description"
    assert dataset.key_attribute_names == ("tamr_id",)


@responses.activate
def test_from_resource_id_dataset_not_found():
    s = fake.session()
    instance = fake.instance()

    url = tc.URL(path="datasets/1")
    responses.add(responses.GET, str(url), status=404)

    with pytest.raises(tc.dataset.NotFound):
        tc.dataset.from_resource_id(s, instance, "1")


@responses.activate
def test_attributes():
    s = fake.session()
    dataset = fake.dataset()

    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")
    attrs_json = utils.load_json("attributes.json")
    responses.add(responses.GET, str(attrs_url), json=attrs_json, status=204)

    attrs = tc.dataset.attributes(s, dataset)

    row_num = attrs[0]
    assert row_num.name == "RowNum"
    assert row_num.type == tc.attribute.type.STRING

    geom = attrs[1]
    assert geom.name == "geom"
    assert isinstance(geom.type, tc.attribute.type.Record)

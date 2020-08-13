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

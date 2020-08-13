import pytest
import responses

import tamr_client as tc
from tests.tamr_client import fake, utils


@responses.activate
def test_from_project():
    s = fake.session()
    instance = fake.instance()
    project = fake.mastering_project()

    dataset_json = utils.load_json("dataset.json")
    url = tc.URL(path="projects/1/unifiedDataset")
    responses.add(responses.GET, str(url), json=dataset_json)

    unified_dataset = tc.dataset.unified.from_project(s, instance, project)
    assert unified_dataset.name == "dataset 1 name"
    assert unified_dataset.description == "dataset 1 description"
    assert unified_dataset.key_attribute_names == ("tamr_id",)


@responses.activate
def test_from_project_dataset_not_found():
    s = fake.session()
    instance = fake.instance()
    project = fake.mastering_project()

    url = tc.URL(path="projects/1/unifiedDataset")
    responses.add(responses.GET, str(url), status=404)

    with pytest.raises(tc.dataset.unified.NotFound):
        tc.dataset.unified.from_project(s, instance, project)


@responses.activate
def test_apply_changes():
    s = fake.session()
    dataset_json = utils.load_json("dataset.json")
    dataset_url = tc.URL(path="projects/1/unifiedDataset")
    unified_dataset = tc.dataset.unified._from_json(dataset_url, dataset_json)

    operation_json = utils.load_json("operation_pending.json")
    operation_url = tc.URL(path="operations/1")
    url = tc.URL(path="projects/1/unifiedDataset:refresh")
    responses.add(responses.POST, str(url), json=operation_json)

    response = tc.dataset.unified._apply_changes_async(s, unified_dataset)
    assert response == tc.operation._from_json(operation_url, operation_json)

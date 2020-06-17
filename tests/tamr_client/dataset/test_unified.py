import pytest
import responses

import tamr_client as tc
from tests.tamr_client import utils


@responses.activate
def test_from_project():
    s = utils.session()
    instance = utils.instance()
    project = utils.mastering_project()

    dataset_json = utils.load_json("dataset.json")
    url = tc.URL(path="projects/1/unifiedDataset")
    responses.add(responses.GET, str(url), json=dataset_json)

    unified_dataset = tc.dataset.unified.from_project(s, instance, project)
    assert unified_dataset.name == "dataset 1 name"
    assert unified_dataset.description == "dataset 1 description"
    assert unified_dataset.key_attribute_names == ("tamr_id",)


@responses.activate
def test_from_project_dataset_not_found():
    s = utils.session()
    instance = utils.instance()
    project = utils.mastering_project()

    url = tc.URL(path="projects/1/unifiedDataset")
    responses.add(responses.GET, str(url), status=404)

    with pytest.raises(tc.dataset.unified.NotFound):
        tc.dataset.unified.from_project(s, instance, project)


@responses.activate
def test_commit():
    s = utils.session()
    instance = utils.instance()
    project = utils.mastering_project()

    operation_json = utils.load_json("operation_pending.json")
    dataset_json = utils.load_json("dataset.json")
    prj_url = tc.URL(path="projects/1/unifiedDataset")
    responses.add(responses.GET, str(prj_url), json=dataset_json)
    unified_dataset = tc.dataset.unified.from_project(s, instance, project)

    url = tc.URL(path="projects/1/unifiedDataset:refresh")
    responses.add(responses.POST, str(url), json=operation_json)

    response = tc.dataset.unified.commit(s, unified_dataset)
    assert response == operation_json

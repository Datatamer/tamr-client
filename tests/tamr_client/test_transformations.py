import pytest
import responses

import tamr_client as tc
from tests.tamr_client import utils


@responses.activate
def test_get_all():
    s = utils.session()
    instance = utils.instance()

    project_json = utils.load_json("mastering_project.json")
    project_url = tc.URL(path="projects/1")
    responses.add(responses.GET, str(project_url), json=project_json)

    tx_json = utils.load_json("transformations.json")
    tx_url = tc.URL(path="projects/1/transformations")
    responses.add(responses.GET, str(tx_url), json=tx_json)

    dataset_json = utils.load_json("dataset.json")
    dataset_url = tc.URL(path="datasets/1")
    responses.add(responses.GET, str(dataset_url), json=dataset_json)

    project = tc.project.from_resource_id(s, instance, "1")
    transforms = tc.transformations.get_all(s, project)

    assert isinstance(transforms, tc.Transformations)

    assert len(transforms.input_scope) == 2
    assert len(transforms.unified_scope) == 1
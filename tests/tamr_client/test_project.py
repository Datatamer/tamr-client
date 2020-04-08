import pytest
import responses

import tamr_client as tc
import tests.tamr_client.utils as utils


@responses.activate
def test_from_resource_id_mastering():
    s = utils.session()
    instance = utils.instance()

    project_json = utils.load_json("mastering_project.json")
    url = tc.URL(path="projects/1")
    responses.add(responses.GET, str(url), json=project_json)

    project = tc.project.from_resource_id(s, instance, "1")
    assert isinstance(project, tc.mastering.Project)
    assert project.name == "proj"
    assert project.description == "Mastering Project"


@responses.activate
def test_from_resource_id_not_found():
    s = utils.session()
    instance = utils.instance()

    url = tc.URL(path="projects/1")
    responses.add(responses.GET, str(url), status=404)

    with pytest.raises(tc.project.NotFound):
        tc.project.from_resource_id(s, instance, "1")

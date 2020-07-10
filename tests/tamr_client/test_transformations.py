import pytest
from requests import HTTPError
import responses

import tamr_client as tc
from tests.tamr_client import utils


@responses.activate
def test_get_all():
    # setup
    project_json = utils.load_json("mastering_project.json")
    project_url = tc.URL(path="projects/1")
    responses.add(responses.GET, str(project_url), json=project_json)

    tx_json = utils.load_json("transformations.json")
    tx_url = tc.URL(path="projects/1/transformations")
    responses.add(responses.GET, str(tx_url), json=tx_json)

    dataset_json = utils.load_json("dataset.json")
    dataset_url = tc.URL(path="datasets/1")
    responses.add(responses.GET, str(dataset_url), json=dataset_json)

    # test
    s = utils.session()
    instance = utils.instance()
    project = tc.project.from_resource_id(s, instance, "1")

    transforms = tc.transformations.get_all(s, project)

    assert isinstance(transforms, tc.Transformations)

    assert len(transforms.input_scope) == 2
    assert len(transforms.unified_scope) == 1

    assert len(transforms.input_scope[0].datasets) == 0
    assert transforms.input_scope[0].transformation == "SELECT *, 1 as one;"
    assert len(transforms.input_scope[1].datasets) == 1
    assert transforms.input_scope[1].datasets[0].name == "dataset 1 name"
    assert transforms.input_scope[1].transformation == "SELECT *, 2 as two;"

    assert transforms.unified_scope[0] == "//Comment\nSELECT *;"


@responses.activate
def test_replace_all():
    # setup
    project_json = utils.load_json("mastering_project.json")
    project_url = tc.URL(path="projects/1")
    responses.add(responses.GET, str(project_url), json=project_json)

    tx_json = utils.load_json("transformations.json")
    tx_url = tc.URL(path="projects/1/transformations")
    responses.add(responses.GET, str(tx_url), json=tx_json)

    dataset_json = utils.load_json("dataset.json")
    dataset_url = tc.URL(path="datasets/1")
    responses.add(responses.GET, str(dataset_url), json=dataset_json)

    # test
    s = utils.session()
    instance = utils.instance()
    project = tc.project.from_resource_id(s, instance, "1")

    transforms = tc.transformations._from_json(s, instance, tx_json)
    transforms.unified_scope.append("//extra TX")
    transforms.input_scope.pop(1)

    responses.add(
        responses.PUT, str(tx_url), json=tc.transformations._to_json(transforms)
    )

    r = tc.transformations.replace_all(s, project, transforms)

    posted_tx = tc.transformations._from_json(s, project.url.instance, r.json())

    assert isinstance(posted_tx, tc.Transformations)

    assert len(posted_tx.input_scope) == 1
    assert len(posted_tx.unified_scope) == 2

    assert len(posted_tx.input_scope[0].datasets) == 0
    assert posted_tx.input_scope[0].transformation == "SELECT *, 1 as one;"

    assert posted_tx.unified_scope[0] == "//Comment\nSELECT *;"
    assert posted_tx.unified_scope[1] == "//extra TX"


@responses.activate
def test_replace_all_errors():
    # setup
    project_json = utils.load_json("mastering_project.json")
    project_url = tc.URL(path="projects/1")
    responses.add(responses.GET, str(project_url), json=project_json)

    tx_json = utils.load_json("transformations.json")
    tx_url = tc.URL(path="projects/1/transformations")
    responses.add(responses.GET, str(tx_url), json=tx_json)

    dataset_json = utils.load_json("dataset.json")
    dataset_url = tc.URL(path="datasets/1")
    responses.add(responses.GET, str(dataset_url), json=dataset_json)

    # test
    s = utils.session()
    instance = utils.instance()
    project = tc.project.from_resource_id(s, instance, "1")

    transforms = tc.transformations._from_json(s, instance, tx_json)

    bad_dataset_err = (
        '{"status": 400, "class": "java.lang.IllegalArgumentException", '
        '"message": "Could not find dataset d1 in this project", "stackTrace": ""}'
    )
    lint_err = (
        '{"status": 400, "class": "javax.ws.rs.BadRequestException", '
        '"message": "------ ERROR ------\\n\\n       mismatched input", "stackTrace": ""}'
    )
    other_err = (
        '{"status": 400, "class": "anything.else", '
        '"message": "A bad thing happened.", "stackTrace": ""}'
    )

    responses.add(responses.PUT, str(tx_url), status=400, body=bad_dataset_err)
    responses.add(responses.PUT, str(tx_url), status=400, body=lint_err)
    responses.add(responses.PUT, str(tx_url), status=400, body=other_err)
    responses.add(responses.PUT, str(tx_url), status=403)

    with pytest.raises(tc.transformations.InvalidInputDataset):
        tc.transformations.replace_all(s, project, transforms)

    with pytest.raises(tc.transformations.LintingError):
        tc.transformations.replace_all(s, project, transforms)

    with pytest.raises(HTTPError):
        tc.transformations.replace_all(s, project, transforms)

    with pytest.raises(HTTPError):
        tc.transformations.replace_all(s, project, transforms)

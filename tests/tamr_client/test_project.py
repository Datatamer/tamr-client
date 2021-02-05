import pytest

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_by_resource_id_mastering():
    s = fake.session()
    instance = fake.instance()

    project = tc.project.by_resource_id(s, instance, "1")
    assert isinstance(project, tc.MasteringProject)
    assert project.name == "proj"
    assert project.description == "Mastering Project"


@fake.json
def test_by_resource_id_categorization():
    s = fake.session()
    instance = fake.instance()

    project = tc.project.by_resource_id(s, instance, "2")
    assert isinstance(project, tc.CategorizationProject)
    assert project.name == "Party Categorization"
    assert project.description == "Categorizes organization at the Party/Domestic level"


@fake.json
def test_by_resource_id_not_found():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.project.NotFound):
        tc.project.by_resource_id(s, instance, "1")


@fake.json
def test_by_name():
    s = fake.session()
    instance = fake.instance()

    project = tc.project.by_name(s, instance, "proj")
    assert project.name == "proj"
    assert project.description == "Mastering Project"


@fake.json
def test_by_name_project_not_found():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.project.NotFound):
        tc.project.by_name(s, instance, "missing project")


@fake.json
def test_by_name_project_ambiguous():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.project.Ambiguous):
        tc.project.by_name(s, instance, "ambiguous project")


@fake.json
def test_get_all():
    s = fake.session()
    instance = fake.instance()

    all_projects = tc.project.get_all(s, instance)
    assert len(all_projects) == 2

    project_1 = all_projects[0]
    assert isinstance(project_1, tc.MasteringProject)
    assert project_1.name == "project 1"
    assert project_1.description == "Mastering Project"

    project_2 = all_projects[1]
    assert isinstance(project_2, tc.CategorizationProject)
    assert project_2.name == "project 2"
    assert project_2.description == "Categorization Project"


@fake.json
def test_get_all_filter():
    s = fake.session()
    instance = fake.instance()

    all_projects = tc.project.get_all(
        s, instance, filter="description==Categorization Project"
    )
    assert len(all_projects) == 1

    project = all_projects[0]
    assert isinstance(project, tc.CategorizationProject)
    assert project.name == "project 2"
    assert project.description == "Categorization Project"


@fake.json
def test_get_all_filter_list():
    s = fake.session()
    instance = fake.instance()

    all_projects = tc.project.get_all(
        s, instance, filter=["description==Categorization Project", "name==project 2"]
    )
    assert len(all_projects) == 1

    project = all_projects[0]
    assert isinstance(project, tc.CategorizationProject)
    assert project.name == "project 2"
    assert project.description == "Categorization Project"


@fake.json
def test_create_project_already_exists():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.project.AlreadyExists):
        tc.project._create(
            s,
            instance,
            name="New Mastering Project",
            project_type="DEDUP",
            description="A Mastering Project",
        )


def test_from_json_unrecognized_project_type():
    instance = fake.instance()
    url = tc.URL("project/1", instance)
    data: tc._types.JsonDict = {
        "id": "unify://unified-data/v1/projects/1",
        "name": "project 1",
        "description": "A project of unknown type",
        "type": "UNKNOWN",
        "unifiedDatasetName": "",
        "relativeId": "projects/1",
        "externalId": "58bdbe72-3c08-427d-97bd-45b16d92c79c",
    }
    project = tc.project._from_json(url, data)
    assert isinstance(project, tc.UnknownProject)
    assert project.name == "project 1"
    assert project.description == "A project of unknown type"

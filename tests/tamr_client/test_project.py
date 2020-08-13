import pytest

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_from_resource_id_mastering():
    s = fake.session()
    instance = fake.instance()

    project = tc.project.from_resource_id(s, instance, "1")
    assert isinstance(project, tc.MasteringProject)
    assert project.name == "proj"
    assert project.description == "Mastering Project"


@fake.json
def test_from_resource_id_categorization():
    s = fake.session()
    instance = fake.instance()

    project = tc.project.from_resource_id(s, instance, "2")
    assert isinstance(project, tc.CategorizationProject)
    assert project.name == "Party Categorization"
    assert project.description == "Categorizes organization at the Party/Domestic level"


@fake.json
def test_from_resource_id_not_found():
    s = fake.session()
    instance = fake.instance()

    with pytest.raises(tc.project.NotFound):
        tc.project.from_resource_id(s, instance, "1")

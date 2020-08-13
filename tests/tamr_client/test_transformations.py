import pytest
from requests import HTTPError

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_get_all():
    s = fake.session()
    project = fake.mastering_project()

    transforms = tc.transformations.get_all(s, project)

    assert len(transforms.input_scope) == 2
    assert len(transforms.unified_scope) == 1

    assert len(transforms.input_scope[0].datasets) == 0
    assert transforms.input_scope[0].transformation == "SELECT *, 1 as one;"
    assert len(transforms.input_scope[1].datasets) == 1
    assert transforms.input_scope[1].datasets[0].name == "dataset 1 name"
    assert transforms.input_scope[1].transformation == "SELECT *, 2 as two;"

    assert transforms.unified_scope[0] == "//Comment\nSELECT *;"


@fake.json
def test_replace_all():
    s = fake.session()
    project = fake.mastering_project()
    transforms = fake.transforms()

    transforms.unified_scope.append("//extra TX")
    transforms.input_scope.pop(1)
    tc.transformations.replace_all(s, project, transforms)


@fake.json
def test_replace_all_errors():
    s = fake.session()
    project = fake.mastering_project()
    transforms = fake.transforms()

    with pytest.raises(HTTPError):
        tc.transformations.replace_all(s, project, transforms)

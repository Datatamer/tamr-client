import pytest

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_from_project():
    s = fake.session()
    project = fake.mastering_project()

    unified_dataset = tc.dataset.unified.from_project(s, project)
    assert unified_dataset.name == "dataset 1 name"
    assert unified_dataset.description == "dataset 1 description"
    assert unified_dataset.key_attribute_names == ("tamr_id",)


@fake.json
def test_from_project_dataset_not_found():
    s = fake.session()
    project = fake.mastering_project()

    with pytest.raises(tc.dataset.unified.NotFound):
        tc.dataset.unified.from_project(s, project)


@fake.json
def test_apply_changes_async():
    s = fake.session()
    unified_dataset = fake.unified_dataset()

    op = tc.dataset.unified._apply_changes_async(s, unified_dataset)
    assert op.type == "SPARK"
    assert op.description == "operation 1 description"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }

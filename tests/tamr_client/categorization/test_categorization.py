import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_manual_labels():
    s = fake.session()
    project = fake.categorization_project()

    tc.categorization.manual_labels(session=s, project=project)


@fake.json
def test_apply_feedback_async():
    s = fake.session()
    project = fake.categorization_project()

    op = tc.categorization._apply_feedback_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Materialize views to Elastic"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_update_results_async():
    s = fake.session()
    project = fake.categorization_project()

    op = tc.categorization._update_results_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Materialize views to Elastic"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }

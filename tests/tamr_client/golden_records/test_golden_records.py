import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_update_async():
    s = fake.session()
    project = fake.golden_records_project()

    op = tc.golden_records._update_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Updating Golden Records"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_publish_async():
    s = fake.session()
    project = fake.golden_records_project()

    op = tc.golden_records._publish_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Updating published datasets for GoldenRecords module"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }

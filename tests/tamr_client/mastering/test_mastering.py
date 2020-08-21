import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_estimate_pairs_async():
    s = fake.session()
    project = fake.mastering_project()

    op = tc.mastering._estimate_pairs_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "operation 1 description"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_generate_pairs_async():
    s = fake.session()
    project = fake.mastering_project()

    op = tc.mastering._generate_pairs_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Materialize views to Elastic"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_apply_feedback_async():
    s = fake.session()
    project = fake.mastering_project()

    op = tc.mastering._apply_feedback_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Materialize views to Elastic"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_update_pair_results_async():
    s = fake.session()
    project = fake.mastering_project()

    op = tc.mastering._update_pair_results_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Materialize views to Elastic"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_update_high_impact_pairs_async():
    s = fake.session()
    project = fake.mastering_project()

    op = tc.mastering._update_high_impact_pairs_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Materialize views to Elastic"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_update_cluster_results_async():
    s = fake.session()
    project = fake.mastering_project()

    op = tc.mastering._update_cluster_results_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "Materialize views to Elastic"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }


@fake.json
def test_publish_clusters_async():
    s = fake.session()
    project = fake.mastering_project()

    op = tc.mastering._publish_clusters_async(s, project)
    assert op.type == "SPARK"
    assert op.description == "operation 1 description"
    assert op.status == {
        "state": "PENDING",
        "startTime": "",
        "endTime": "",
        "message": "Job has not yet been submitted to Spark",
    }

import os

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tests.mock_api.utils import mock_api


basedir = os.path.dirname(__file__)
response_log_path = os.path.join(
    basedir, "../response_logs/continuous_mastering.ndjson"
)


@mock_api(response_log_path)
def test_continuous_mastering():
    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)

    project_id = "1"
    project = unify.projects.by_resource_id(project_id)
    project = project.as_mastering()

    unified_dataset = project.unified_dataset()
    op = unified_dataset.refresh(poll_interval_seconds=0)
    assert op.succeeded()

    op = project.pairs().refresh(poll_interval_seconds=0)
    assert op.succeeded()

    model = project.pair_matching_model()
    op = model.train(poll_interval_seconds=0)
    assert op.succeeded()

    op = model.predict(poll_interval_seconds=0)
    assert op.succeeded()

    op = project.record_clusters().refresh(poll_interval_seconds=0)
    assert op.succeeded()

    op = project.published_clusters().refresh(poll_interval_seconds=0)
    assert op.succeeded()

    estimate_url = (
        f"http://localhost:9100/api/versioned/v1/projects/1/estimatedPairCounts"
    )
    estimate_json = {
        "isUpToDate": "true",
        "totalEstimate": {"candidatePairCount": "200", "generatedPairCount": "100"},
        "clauseEstimates": {
            "clause1": {"candidatePairCount": "50", "generatedPairCount": "25"},
            "clause2": {"candidatePairCount": "50", "generatedPairCount": "25"},
            "clause3": {"candidatePairCount": "100", "generatedPairCount": "50"},
        },
    }
    responses.add(responses.GET, estimate_url, json=estimate_json)

    status = project.estimate_pairs().is_up_to_date
    assert status

    candidate = project.estimate_pairs().total_estimate["candidatePairCount"]
    assert candidate == "200"

    clause1 = project.estimate_pairs().clause_estimates["clause1"]
    assert clause1["generatedPairCount"] == "25"

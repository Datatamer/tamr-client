import os
import json
import responses

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from .utils import mock_api

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

project_config = {
    "name": "Project 1",
    "description": "Mastering Project",
    "type": "DEDUP",
    "unifiedDatasetName": "Project 1 - Unified Dataset",
    "externalId": "Project1",
    "resourceId": "1",
}

unified_dataset_json = {
    "id": "unify://unified-data/v1/datasets/8",
    "name": "Project_1_unified_dataset",
    "version": "10",
    "relativeId": "datasets/8",
    "externalId": "Project_1_unified_dataset",
}

datasets_json = [
    {
        "id": "unify://unified-data/v1/datasets/36",
        "name": "Project_1_unified_dataset_dedup_clusters_with_data",
        "version": "251",
        "relativeId": "datasets/36",
        "externalId": "1",
    }
]


rcwd_json = {
    "externalId": "1",
    "id": "unify://unified-data/v1/datasets/36",
    "name": "Project_1_unified_dataset_dedup_clusters_with_data",
    "relativeId": "datasets/36",
    "version": "251",
}


@responses.activate
def test_rcwd():

    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)

    project_external_id = "1"

    projects_url = (
        f"http://localhost:9100/api/versioned/v1/projects/{project_external_id}"
    )
    unified_dataset_url = (
        f"http://localhost:9100/api/versioned/v1/projects/1/unifiedDataset"
    )
    datasets_url = f"http://localhost:9100/api/versioned/v1/datasets"

    responses.add(responses.GET, projects_url, json=project_config)
    responses.add(responses.GET, unified_dataset_url, json=unified_dataset_json)
    responses.add(responses.GET, datasets_url, json=datasets_json)

    project = unify.projects.by_resource_id("1")
    actual_rcwd_dataset = project.as_mastering().record_clusters_with_data()
    assert actual_rcwd_dataset._data == rcwd_json

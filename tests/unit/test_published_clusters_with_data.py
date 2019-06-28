import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@responses.activate
def test_published_clusters_with_data():
    project_config = {
        "name": "Project 1",
        "description": "Mastering Project",
        "type": "DEDUP",
        "unifiedDatasetName": "Project_1_unified_dataset",
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

    pcwd_json = {
        "externalId": "1",
        "id": "unify://unified-data/v1/datasets/36",
        "name": "Project_1_unified_dataset_dedup_published_clusters_with_data",
        "relativeId": "datasets/36",
        "version": "251",
    }

    datasets_json = [pcwd_json]

    unify = Client(UsernamePasswordAuth("username", "password"))

    project_id = "1"

    project_url = f"http://localhost:9100/api/versioned/v1/projects/{project_id}"
    unified_dataset_url = (
        f"http://localhost:9100/api/versioned/v1/projects/{project_id}/unifiedDataset"
    )
    datasets_url = f"http://localhost:9100/api/versioned/v1/datasets"

    responses.add(responses.GET, project_url, json=project_config)
    responses.add(responses.GET, unified_dataset_url, json=unified_dataset_json)
    responses.add(responses.GET, datasets_url, json=datasets_json)
    project = unify.projects.by_resource_id(project_id)
    actual_pcwd_dataset = project.as_mastering().published_clusters_with_data()
    assert actual_pcwd_dataset.name == pcwd_json["name"]

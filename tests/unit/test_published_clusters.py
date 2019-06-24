import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@responses.activate
def test_published_clusters():

    project_config_json = {
        "id": "unify://unified-data/v1/projects/1",
        "name": "Project_1",
        "description": "Mastering Project",
        "type": "DEDUP",
        "unifiedDatasetName": "Project_1_unified_dataset",
        "relativeId": "projects/1",
        "externalId": "32b99cab-e01b-41e7-a29d-509165242c6f",
    }

    unified_dataset_json = {
        "id": "unify://unified-data/v1/datasets/8",
        "name": "Project_1_unified_dataset",
        "version": "10",
        "relativeId": "datasets/8",
        "externalId": "Project_1_unified_dataset",
    }

    published_clusters_json = {
        "id": "unify://unified-data/v1/datasets/32",
        "name": "Project_1_unified_dataset_dedup_published_clusters",
        "description": "All the mappings of records to clusters.",
        "version": "253",
        "relativeId": "datasets/32",
        "externalId": "Project_1_unified_dataset_dedup_published_clusters",
    }

    datasets_json = [published_clusters_json]

    refresh_json = {
        "id": "93",
        "type": "SPARK",
        "description": "Publish clusters",
        "status": {
            "state": "PENDING",
            "startTime": "",
            "endTime": "",
            "message": "Job has not yet been submitted to Spark",
        },
        "created": {
            "username": "admin",
            "time": "2019-06-24T15:58:48.734Z",
            "version": "2407",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-06-24T15:58:48.734Z",
            "version": "2407",
        },
        "relativeId": "operations/93",
    }

    operations_json = {
        "id": "93",
        "type": "SPARK",
        "description": "Publish clusters",
        "status": {
            "state": "SUCCEEDED",
            "startTime": "2019-06-24T15:58:56.595Z",
            "endTime": "2019-06-24T15:59:17.084Z",
        },
        "created": {
            "username": "admin",
            "time": "2019-06-24T15:58:48.734Z",
            "version": "2407",
        },
        "lastModified": {
            "username": "system",
            "time": "2019-06-24T15:59:18.350Z",
            "version": "2423",
        },
        "relativeId": "operations/93",
    }

    unify = Client(UsernamePasswordAuth("username", "password"))
    project_id = "1"

    project_url = f"http://localhost:9100/api/versioned/v1/projects/{project_id}"
    unified_dataset_url = (
        f"http://localhost:9100/api/versioned/v1/projects/{project_id}/unifiedDataset"
    )
    datasets_url = f"http://localhost:9100/api/versioned/v1/datasets"
    refresh_url = f"http://localhost:9100/api/versioned/v1/projects/{project_id}/publishedClusters:refresh"
    operations_url = f"http://localhost:9100/api/versioned/v1/operations/93"

    responses.add(responses.GET, project_url, json=project_config_json)
    responses.add(responses.GET, unified_dataset_url, json=unified_dataset_json)
    responses.add(responses.GET, datasets_url, json=datasets_json)
    responses.add(responses.POST, refresh_url, json=refresh_json)
    responses.add(responses.GET, operations_url, json=operations_json)
    project = unify.projects.by_resource_id(project_id)
    actual_published_clusters_dataset = project.as_mastering().published_clusters()
    actual_published_clusters_dataset.refresh()
    assert actual_published_clusters_dataset.name == published_clusters_json["name"]

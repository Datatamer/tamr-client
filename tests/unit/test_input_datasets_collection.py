import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@pytest.fixture
def client():
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    return tamr


@responses.activate
def test_delete_by_resource_id(client):
    input_collection = url_prefix + "projects/1/inputDatasets"
    input_ds = input_collection + "/6"

    responses.add(responses.GET, mastering_project, json=mastering_project_config)

    responses.add(responses.GET, input_collection, json=input_ds_json)
    responses.add(responses.DELETE, input_ds, status=204)

    input_ds_collection = client.projects.by_resource_id("1").input_datasets()
    response = input_ds_collection.delete_by_resource_id("6")
    assert response.status_code == 204


url_prefix = "http://localhost:9100/api/versioned/v1/"
mastering_project = url_prefix + "projects/1"

mastering_project_config = {
    "name": "Project 1",
    "description": "Mastering Project",
    "type": "DEDUP",
    "unifiedDatasetName": "Project 1 - Unified Dataset",
    "externalId": "Project1",
    "resourceId": "1",
}

input_ds_json = [
    {
        "id": "unify://unified-data/v1/datasets/6",
        "name": "febrl_sample_2k.csv",
        "description": "charlotte SM dataset",
        "version": "5",
        "keyAttributeNames": ["rec_id"],
        "tags": [],
        "created": {
            "username": "admin",
            "time": "2019-06-05T16:16:31.964Z",
            "version": "35",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-07-19T17:44:42.369Z",
            "version": "22919",
        },
        "relativeId": "datasets/6",
        "upstreamDatasetIds": [],
        "externalId": "febrl_sample_2k.csv",
    }
]

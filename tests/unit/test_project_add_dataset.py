from functools import partial

import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

dataset_json = [
    {
        "id": "unify://unified-data/v1/datasets/1",
        "externalId": "1",
        "name": "dataset 1 name",
        "description": "dataset 1 description",
        "version": "dataset 1 version",
        "keyAttributeNames": ["tamr_id"],
        "tags": [],
        "created": {
            "username": "admin",
            "time": "2018-09-10T16:06:20.636Z",
            "version": "dataset 1 created version",
        },
        "lastModified": {
            "username": "admin",
            "time": "2018-09-10T16:06:20.851Z",
            "version": "dataset 1 modified version",
        },
        "relativeId": "datasets/1",
        "upstreamDatasetIds": [],
    }
]

dataset_external_id = "1"
datasets_url = f"http://localhost:9100/api/versioned/v1/datasets?filter=externalId=={dataset_external_id}"

project_json = [
    {
        "id": "unify://unified-data/v1/projects/1",
        "externalId": "1",
        "name": "project 1 name",
        "description": "project 1 description",
        "type": "DEDUP",
        "unifiedDatasetName": "project 1 unified dataset",
        "created": {
            "username": "admin",
            "time": "2018-09-10T16:06:20.636Z",
            "version": "project 1 created version",
        },
        "lastModified": {
            "username": "admin",
            "time": "2018-09-10T16:06:20.851Z",
            "version": "project 1 modified version",
        },
        "relativeId": "projects/1",
    }
]

project_external_id = "1"
projects_url = f"http://localhost:9100/api/versioned/v1/projects?filter=externalId=={project_external_id}"

post_input_datasets_json = []
input_datasets_url = f"http://localhost:9100/api/versioned/v1/projects/1/inputDatasets"
get_input_datasets_json = dataset_json


@responses.activate
def test_project_add_source_dataset():
    responses.add(responses.GET, datasets_url, json=dataset_json)
    responses.add(responses.GET, projects_url, json=project_json)
    responses.add(
        responses.POST, input_datasets_url, json=post_input_datasets_json, status=204
    )
    responses.add(responses.GET, input_datasets_url, json=get_input_datasets_json)
    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)
    dataset = unify.datasets.by_external_id(dataset_external_id)
    project = unify.projects.by_external_id(project_external_id)
    project.add_source_dataset(dataset)
    alias = project.api_path + "/inputDatasets"
    input_datasets = project.client.get(alias).successful().json()
    assert input_datasets == dataset_json

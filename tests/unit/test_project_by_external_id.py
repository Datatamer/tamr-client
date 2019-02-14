import json

import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

project_json = [
    {
        "id": "unify://unified-data/v1/projects/1",
        "externalId": "project 1 external ID",
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

project_external_id = "project 1 external ID"
projects_url = f"http://localhost:9100/api/versioned/v1/projects?filter=externalId=={project_external_id}"


@responses.activate
def test_project_by_external_id__raises_when_not_found():
    responses.add(responses.GET, projects_url, json=[])
    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)
    with pytest.raises(KeyError):
        unify.projects.by_external_id(project_external_id)


@responses.activate
def test_project_by_external_id_succeeds():
    responses.add(responses.GET, projects_url, json=project_json)
    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)
    actual_project = unify.projects.by_external_id(project_external_id)
    assert actual_project.data == project_json[0]

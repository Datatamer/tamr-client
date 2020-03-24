import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

project_json = [
  {
    "id": "unify://unified-data/v1/projects/1",
    "name": "project 1 name",
    "description": "project 1 description",
    "type": "DEDUP",
    "unifiedDatasetName": "project 1 name_unified_dataset",
    "created": {
      "username": "admin",
      "time": "2020-03-24T12:43:57.087Z",
      "version": "project 1 created version"
    },
    "lastModified": {
      "username": "admin",
      "time": "2020-03-24T12:43:59.564Z",
      "version": "project 1 modified version"
    },
    "relativeId": "projects/1",
    "externalId": "number 1"
  }
]

project_name = "project 1 name"
projects_url = f"http://localhost:9100/api/versioned/v1/projects"


@responses.activate
def test_project_by_name__raises_when_not_found():
    responses.add(responses.GET, projects_url, json=[])
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    with pytest.raises(KeyError):
        tamr.projects.by_name(project_name)


@responses.activate
def test_dataset_by_name_succeeds():
    responses.add(responses.GET, projects_url, json=project_json)
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    actual_project = tamr.projects.by_name(project_name)
    assert actual_project._data == project_json[0]

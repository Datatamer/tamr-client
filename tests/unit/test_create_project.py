import json

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

auth = UsernamePasswordAuth("username", "password")
unify = Client(auth)


@responses.activate
def test_create_project():
    project_creation_spec = {
        "name": "Project 1",
        "description": "Mastering Project",
        "type": "DEDUP",
        "unifiedDatasetName": "Project 1 - Unified Dataset",
        "externalId": "Project1",
        "resourceId": "1",
    }

    projects_url = f"http://localhost:9100/api/versioned/v1/projects"
    project_url = f"http://localhost:9100/api/versioned/v1/projects/1"

    responses.add(responses.POST, projects_url, json=project_creation_spec, status=204)
    responses.add(responses.GET, project_url, json=project_creation_spec)

    u = unify.create_project(project_creation_spec)
    p = unify.projects.by_resource_id("1")
    assert print(p) == print(u)

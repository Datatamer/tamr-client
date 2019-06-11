import json

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

auth = UsernamePasswordAuth("username", "password")
unify = Client(auth)


@responses.activate
def test_create_project():
    project_config = {
        "name": "Project 1",
        "description": "Mastering Project",
        "type": "DEDUP",
        "unifiedDatasetName": "Project 1 - Unified Dataset",
        "externalId": "Project1",
        "resourceId": "1",
    }

    projects_url = f"http://localhost:9100/api/versioned/v1/projects"
    project_url = f"http://localhost:9100/api/versioned/v1/projects/1"

    responses.add(responses.POST, projects_url, json={}, status=204)
    responses.add(responses.GET, project_url, json=project_config)

    unify.create_project(project_config)
    p = unify.projects.by_resource_id("1")
    print(p)

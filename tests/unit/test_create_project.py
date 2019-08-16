from functools import partial
import json

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.project.resource import ProjectSpec

auth = UsernamePasswordAuth("username", "password")
tamr = Client(auth)

creation_spec = {
    "name": "Project 1",
    "description": "Mastering Project",
    "type": "DEDUP",
    "unifiedDatasetName": "Project 1 - Unified Dataset",
    "externalId": "Project1",
}

project_json = {
    **creation_spec,
    "id": "unify://unified-data/v1/projects/1",
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

projects_url = f"http://localhost:9100/api/versioned/v1/projects"
project_url = f"{projects_url}/1"


@responses.activate
def test_create_project():
    def create_callback(request, snoop):
        snoop["payload"] = json.loads(request.body)
        return 204, {}, json.dumps(project_json)

    snoop_dict = {}
    responses.add_callback(
        responses.POST, projects_url, partial(create_callback, snoop=snoop_dict)
    )
    responses.add(responses.GET, project_url, json=project_json)

    u = tamr.projects.create(creation_spec)
    p = tamr.projects.by_resource_id("1")

    assert snoop_dict["payload"] == creation_spec
    assert p.__repr__() == u.__repr__()


@responses.activate
def test_create_from_spec():
    def create_callback(request, snoop):
        snoop["payload"] = json.loads(request.body)
        return 204, {}, json.dumps(project_json)

    snoop_dict = {}
    responses.add_callback(
        responses.POST, projects_url, partial(create_callback, snoop=snoop_dict)
    )

    spec = (
        ProjectSpec.new()
        .with_name(creation_spec["name"])
        .with_description(creation_spec["description"])
        .with_type(creation_spec["type"])
        .with_unified_dataset_name(creation_spec["unifiedDatasetName"])
        .with_external_id(creation_spec["externalId"])
    )
    p = tamr.projects.create(spec.to_dict())

    assert snoop_dict["payload"] == creation_spec
    assert p.relative_id == project_json["relativeId"]

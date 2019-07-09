from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


class TestProject(TestCase):
    @responses.activate
    def test_project_add_source_dataset(self):
        responses.add(responses.GET, self.datasets_url, json=self.dataset_json)
        responses.add(responses.GET, self.projects_url, json=self.project_json)
        responses.add(
            responses.POST,
            self.input_datasets_url,
            json=self.post_input_datasets_json,
            status=204,
        )
        responses.add(
            responses.GET, self.input_datasets_url, json=self.get_input_datasets_json
        )
        auth = UsernamePasswordAuth("username", "password")
        unify = Client(auth)
        dataset = unify.datasets.by_external_id(self.dataset_external_id)
        project = unify.projects.by_external_id(self.project_external_id)
        project.add_source_dataset(dataset)
        alias = project.api_path + "/inputDatasets"
        input_datasets = project.client.get(alias).successful().json()
        assert input_datasets == self.dataset_json

    dataset_external_id = "1"
    datasets_url = f"http://localhost:9100/api/versioned/v1/datasets?filter=externalId=={dataset_external_id}"
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
    input_datasets_url = (
        f"http://localhost:9100/api/versioned/v1/projects/1/inputDatasets"
    )
    get_input_datasets_json = dataset_json

from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.models.project.resource import Project


class PublishedClusterTest(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_published_clusters(self):
        datasets_json = [self._published_clusters_json]
        project_id = "1"

        project_url = f"http://localhost:9100/api/versioned/v1/projects/{project_id}"
        unified_dataset_url = f"http://localhost:9100/api/versioned/v1/projects/{project_id}/unifiedDataset"
        datasets_url = f"http://localhost:9100/api/versioned/v1/datasets"
        refresh_url = f"http://localhost:9100/api/versioned/v1/projects/{project_id}/publishedClusters:refresh"
        operations_url = f"http://localhost:9100/api/versioned/v1/operations/93"

        responses.add(responses.GET, project_url, json=self._project_config_json)
        responses.add(
            responses.GET, unified_dataset_url, json=self._unified_dataset_json
        )
        responses.add(responses.GET, datasets_url, json=datasets_json)
        responses.add(responses.POST, refresh_url, json=self._refresh_json)
        responses.add(responses.GET, operations_url, json=self._operations_json)
        project = self.unify.projects.by_resource_id(project_id)
        actual_published_clusters_dataset = project.as_mastering().published_clusters()
        actual_published_clusters_dataset.refresh()
        self.assertEqual(
            actual_published_clusters_dataset.name,
            self._published_clusters_json["name"],
        )

    @responses.activate
    def test_published_clusters_configuration(self):
        config_url = f"http://localhost:9100/api/versioned/v1/projects/1/publishedClustersConfiguration"
        responses.add(responses.GET, config_url, json=self._config_json)

        p = Project(self.unify, self._project_config_json, "projects/1").as_mastering()
        config = p.published_clusters_configuration()

        self.assertEqual(config, self._config_json)

    _project_config_json = {
        "id": "unify://unified-data/v1/projects/1",
        "name": "Project_1",
        "description": "Mastering Project",
        "type": "DEDUP",
        "unifiedDatasetName": "Project_1_unified_dataset",
        "relativeId": "projects/1",
        "externalId": "32b99cab-e01b-41e7-a29d-509165242c6f",
    }

    _unified_dataset_json = {
        "id": "unify://unified-data/v1/datasets/8",
        "name": "Project_1_unified_dataset",
        "version": "10",
        "relativeId": "datasets/8",
        "externalId": "Project_1_unified_dataset",
    }

    _published_clusters_json = {
        "id": "unify://unified-data/v1/datasets/32",
        "name": "Project_1_unified_dataset_dedup_published_clusters",
        "description": "All the mappings of records to clusters.",
        "version": "253",
        "relativeId": "datasets/32",
        "externalId": "Project_1_unified_dataset_dedup_published_clusters",
    }

    _refresh_json = {
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

    _operations_json = {
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

    _config_json = {"versionsTimeToLive": "P4D"}

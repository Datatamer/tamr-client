from unittest import TestCase

from requests import HTTPError
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.mastering.published_cluster.configuration import (
    PublishedClustersConfiguration,
)
from tamr_unify_client.project.resource import Project


class PublishedClusterTest(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    @responses.activate
    def test_published_clusters(self):
        project_id = "1"
        project_url = f"{self._base_url}/projects/{project_id}"
        unified_dataset_url = f"{self._base_url}/projects/{project_id}/unifiedDataset"
        datasets_url = f"{self._base_url}/datasets"
        refresh_url = (
            f"{self._base_url}/projects/{project_id}/publishedClusters:refresh"
        )
        operations_url = f"{self._base_url}/operations/93"

        responses.add(responses.GET, project_url, json=self._project_config_json)
        responses.add(
            responses.GET, unified_dataset_url, json=self._unified_dataset_json
        )
        responses.add(responses.GET, datasets_url, json=self._datasets_json)
        responses.add(responses.POST, refresh_url, json=self._refresh_json)
        responses.add(responses.GET, operations_url, json=self._operations_json)
        project = self.unify.projects.by_resource_id(project_id)
        actual_published_clusters_dataset = project.as_mastering().published_clusters()
        actual_published_clusters_dataset.refresh(poll_interval_seconds=0)
        self.assertEqual(
            actual_published_clusters_dataset.name,
            self._published_clusters_json["name"],
        )

    @responses.activate
    def test_published_clusters_configuration(self):
        path = "projects/1/publishedClustersConfiguration"
        config_url = f"{self._base_url}/{path}"
        responses.add(responses.GET, config_url, json=self._config_json)

        p = Project(self.unify, self._project_config_json).as_mastering()
        config = p.published_clusters_configuration()
        created = PublishedClustersConfiguration.from_json(
            self.unify, self._config_json, path
        )

        self.assertEqual(repr(config), repr(created))
        self.assertEqual(
            config.versions_time_to_live, self._config_json["versionsTimeToLive"]
        )

    @responses.activate
    def test_delete_published_clusters_configuration(self):
        path = "projects/1/publishedClustersConfiguration"
        config_url = f"{self._base_url}/{path}"
        responses.add(responses.GET, config_url, json=self._config_json)
        responses.add(responses.DELETE, config_url, status=405)

        p = Project(self.unify, self._project_config_json).as_mastering()
        config = p.published_clusters_configuration()
        self.assertRaises(HTTPError, config.delete)

    @responses.activate
    def test_refresh_ids(self):
        unified_dataset_url = f"{self._base_url}/projects/1/unifiedDataset"
        datasets_url = f"{self._base_url}/datasets"
        refresh_url = f"{self._base_url}/projects/1/allPublishedClusterIds:refresh"

        responses.add(
            responses.GET, unified_dataset_url, json=self._unified_dataset_json
        )
        responses.add(responses.GET, datasets_url, json=self._datasets_json)
        responses.add(responses.POST, refresh_url, json=self._operations_json)

        p = Project(self.unify, self._project_config_json).as_mastering()
        d = p.published_cluster_ids()

        op = d.refresh(poll_interval_seconds=0)
        self.assertEqual(op.resource_id, self._operations_json["id"])
        self.assertTrue(op.succeeded())

    @responses.activate
    def test_refresh_stats(self):
        unified_dataset_url = f"{self._base_url}/projects/1/unifiedDataset"
        datasets_url = f"{self._base_url}/datasets"
        refresh_url = f"{self._base_url}/projects/1/publishedClusterStats:refresh"

        responses.add(
            responses.GET, unified_dataset_url, json=self._unified_dataset_json
        )
        responses.add(responses.GET, datasets_url, json=self._datasets_json)
        responses.add(responses.POST, refresh_url, json=self._operations_json)

        p = Project(self.unify, self._project_config_json).as_mastering()
        d = p.published_cluster_stats()

        op = d.refresh(poll_interval_seconds=0)
        self.assertEqual(op.resource_id, self._operations_json["id"])
        self.assertTrue(op.succeeded())

    _base_url = "http://localhost:9100/api/versioned/v1"

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

    _published_stats_json = {
        "id": "unify://unified-data/v1/datasets/33",
        "name": "Project_1_unified_dataset_dedup_published_cluster_stats",
        "description": "Published cluster stats",
        "version": "253",
        "relativeId": "datasets/33",
        "externalId": "Project_1_unified_dataset_dedup_published_cluster_stats",
    }

    _published_ids_json = {
        "id": "unify://unified-data/v1/datasets/34",
        "name": "Project_1_unified_dataset_dedup_all_persistent_ids",
        "description": "All previously and currently published cluster IDs",
        "version": "253",
        "relativeId": "datasets/34",
        "externalId": "Project_1_unified_dataset_dedup_all_persistent_ids",
    }

    _datasets_json = [
        _unified_dataset_json,
        _published_clusters_json,
        _published_stats_json,
        _published_ids_json,
    ]

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

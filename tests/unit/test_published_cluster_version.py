from functools import partial
import json
from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client.mastering.published_cluster.metric import Metric
from tamr_unify_client.mastering.published_cluster.resource import PublishedCluster
from tamr_unify_client.mastering.published_cluster.version import (
    PublishedClusterVersion,
)
from tamr_unify_client.project.resource import Project


class PublishedClusterTest(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.unify = Client(auth)

    def test_metric(self):
        metric_json = {"metricName": "recordCount", "metricValue": "1"}
        m = Metric(metric_json)
        self.assertEqual(m.name, metric_json["metricName"])
        self.assertEqual(m.value, metric_json["metricValue"])

    def test_cluster_version(self):
        version_json = self._versions_json[0]["versions"][0]
        version = PublishedClusterVersion(version_json)

        self.assertEqual(version.version, version_json["version"])
        self.assertEqual(version.timestamp, version_json["timestamp"])
        self.assertEqual(version.name, version_json["name"])
        self.assertEqual(version.record_ids, version_json["recordIds"])

        metrics = [Metric(m) for m in version_json["metrics"]]
        for actual, expected in zip(version.metrics, metrics):
            self.assertEqual(actual.__repr__(), expected.__repr__())

    def test_cluster(self):
        cluster_json = self._versions_json[0]
        cluster = PublishedCluster(cluster_json)
        versions = cluster.versions
        expected_versions = [
            PublishedClusterVersion(v) for v in cluster_json["versions"]
        ]

        self.assertEqual(cluster.id, cluster_json["id"])
        self.assertEqual(len(versions), len(expected_versions))
        for actual, expected in zip(versions, expected_versions):
            self.assertEqual(actual.__repr__(), expected.__repr__())

    @responses.activate
    def test_get_versions(self):
        def create_callback(request, snoop):
            snoop["payload"] = request.body
            return 200, {}, "\n".join(json.dumps(c) for c in self._versions_json)

        p = Project.from_json(self.unify, self._project_json).as_mastering()
        post_url = f"http://localhost:9100/api/versioned/v1/{p.api_path}/publishedClusterVersions"
        snoop = {}
        responses.add_callback(
            responses.POST, post_url, partial(create_callback, snoop=snoop)
        )

        clusters = list(p.published_cluster_versions(self._cluster_ids))
        expected_clusters = [PublishedCluster(c) for c in self._versions_json]

        self.assertEqual(
            snoop["payload"], "\n".join([json.dumps(i) for i in self._cluster_ids])
        )
        self.assertEqual(len(clusters), len(expected_clusters))
        for actual, expected in zip(clusters, expected_clusters):
            self.assertEqual(actual.__repr__(), expected.__repr__())
            self.assertEqual(len(actual.versions), len(expected.versions))

    _project_json = {
        "id": "unify://unified-data/v1/projects/1",
        "name": "Test Project",
        "description": "Mastering Project",
        "type": "DEDUP",
        "unifiedDatasetName": "",
        "created": {
            "username": "admin",
            "time": "2019-07-12T13:08:17.440Z",
            "version": "401",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-07-12T13:08:17.534Z",
            "version": "402",
        },
        "relativeId": "projects/1",
        "externalId": "904bf89e-74ba-45c5-8b4a-5ff913728f66",
    }

    _cluster_ids = [
        "055908e7-2144-3f46-ba21-4c2e58816228",
        "ca68d64b-755e-32b7-a785-5f9b1f51e420",
    ]

    _versions_json = [
        {
            "id": "055908e7-2144-3f46-ba21-4c2e58816228",
            "versions": [
                {
                    "version": 324,
                    "timestamp": "2019-07-17T15:48:40.171Z",
                    "name": "cluster 1",
                    "metrics": [
                        {"metricName": "recordCount", "metricValue": "2"},
                        {"metricName": "totalSpend", "metricValue": "0.0"},
                        {"metricName": "verifiedRecordCount", "metricValue": "0"},
                        {
                            "metricName": "averageLinkage",
                            "metricValue": "0.7626373626373626",
                        },
                    ],
                    "recordIds": [
                        {
                            "entityId": "6084737977926081128",
                            "originSourceId": "dataset_name",
                            "originEntityId": "82049",
                        },
                        {
                            "entityId": "-3832930559140320929",
                            "originSourceId": "dataset_name",
                            "originEntityId": "80455",
                        },
                    ],
                },
                {
                    "version": 323,
                    "timestamp": "2019-07-15T15:48:40.171Z",
                    "name": "cluster 1",
                    "metrics": [
                        {"metricName": "recordCount", "metricValue": "1"},
                        {"metricName": "totalSpend", "metricValue": "0.0"},
                        {"metricName": "verifiedRecordCount", "metricValue": "0"},
                        {
                            "metricName": "averageLinkage",
                            "metricValue": "0.7626373626373626",
                        },
                    ],
                    "recordIds": [
                        {
                            "entityId": "6084737977926081128",
                            "originSourceId": "dataset_name",
                            "originEntityId": "82049",
                        }
                    ],
                },
            ],
        },
        {
            "id": "ca68d64b-755e-32b7-a785-5f9b1f51e420",
            "versions": [
                {
                    "version": 324,
                    "timestamp": "2019-07-17T15:48:40.171Z",
                    "name": "cluster 2",
                    "metrics": [
                        {"metricName": "recordCount", "metricValue": "1"},
                        {"metricName": "totalSpend", "metricValue": "0.0"},
                        {"metricName": "verifiedRecordCount", "metricValue": "0"},
                        {
                            "metricName": "averageLinkage",
                            "metricValue": "0.7582417582417584",
                        },
                    ],
                    "recordIds": [
                        {
                            "entityId": "-4650342988873587155",
                            "originSourceId": "dataset_name",
                            "originEntityId": "63730",
                        }
                    ],
                }
            ],
        },
    ]

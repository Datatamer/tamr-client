from unittest import TestCase

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


class TestDatasetProfile(TestCase):
    @responses.activate
    def test_dataset_profile(self):
        auth = UsernamePasswordAuth("username", "password")
        client = Client(auth)

        dataset_id = "3"
        dataset_url = f"{client.protocol}://{client.host}:{client.port}/api/versioned/v1/datasets/{dataset_id}"
        profile_url = f"{dataset_url}/profile"
        responses.add(responses.GET, dataset_url, json={})
        responses.add(responses.GET, profile_url, json=self.profile_stale)

        dataset = client.datasets.by_resource_id(dataset_id)
        profile = dataset.profile()
        self.assertEqual(self.profile_stale["datasetName"], profile.dataset_name)
        self.assertEqual(
            self.profile_stale["relativeDatasetId"], profile.relative_dataset_id
        )
        self.assertEqual(self.profile_stale["isUpToDate"], profile.is_up_to_date)
        self.assertEqual(
            self.profile_stale["profiledDataVersion"], profile.profiled_data_version
        )
        self.assertEqual(self.profile_stale["profiledAt"], profile.profiled_at)
        self.assertEqual(self.profile_stale["simpleMetrics"], profile.simple_metrics)
        self.assertEqual(
            self.profile_stale["attributeProfiles"], profile.attribute_profiles
        )

    @responses.activate
    def test_profile_refresh(self):
        auth = UsernamePasswordAuth("username", "password")
        client = Client(auth)

        dataset_id = "3"
        dataset_url = f"{client.protocol}://{client.host}:{client.port}/api/versioned/v1/datasets/{dataset_id}"
        profile_url = f"{dataset_url}/profile"
        profile_refresh_url = f"{profile_url}:refresh"
        responses.add(responses.GET, dataset_url, json={})
        responses.add(responses.GET, profile_url, json=self.profile_stale)
        responses.add(
            responses.POST, profile_refresh_url, json=self.operation_succeeded
        )

        dataset = client.datasets.by_resource_id(dataset_id)
        profile = dataset.profile()
        op = profile.refresh()
        self.assertTrue(op.succeeded())

    @responses.activate
    def test_profile_create(self):
        auth = UsernamePasswordAuth("username", "password")
        client = Client(auth)

        dataset_id = "3"
        dataset_url = f"{client.protocol}://{client.host}:{client.port}/api/versioned/v1/datasets/{dataset_id}"
        profile_url = f"{dataset_url}/profile"
        profile_refresh_url = f"{profile_url}:refresh"
        responses.add(responses.GET, dataset_url, json={})
        # We need to ensure that, when creating the profile,
        # nothing ever tries to access the (non-existent) profile.
        responses.add(responses.GET, profile_url, status=404)
        responses.add(
            responses.POST, profile_refresh_url, json=self.operation_succeeded
        )

        dataset = client.datasets.by_resource_id(dataset_id)
        op = dataset.create_profile()
        self.assertTrue(op.succeeded())

    profile_stale = {
        "datasetName": "ds3",
        "relativeDatasetId": "v1/datasets/3",
        "isUpToDate": False,
        "profiledDataVersion": "3",
        "profiledAt": {
            "username": "system",
            "time": "2019-06-05T14:23:25.860Z",
            "version": "46",
        },
        "simpleMetrics": [{"metricName": "rowCount", "metricValue": "1999"}],
        "attributeProfiles": [
            {
                "attributeName": "attribute1",
                "simpleMetrics": [
                    {"metricName": "distinctValueCount", "metricValue": "1999"}
                ],
                "mostFrequentValues": [
                    {"value": "value1", "frequency": "1999", "percentFrequency": 1.0}
                ],
            }
        ],
    }

    operation_succeeded = {
        "id": "1",
        "type": "SPARK",
        "description": "Synthetic Operation",
        "status": {
            "state": "SUCCEEDED",
            "startTime": "2018-12-14T19:34:00.273Z",
            "endTime": "2018-12-14T19:34:14.573Z",
            "message": "",
        },
        "created": {
            "username": "admin",
            "time": "2018-12-14T19:33:50.538Z",
            "version": "390",
        },
        "lastModified": {
            "username": "system",
            "time": "2018-12-14T19:34:15.200Z",
            "version": "399",
        },
        "relativeId": "operations/1",
    }

from unittest import TestCase

from requests import HTTPError
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


class TestAttribute(TestCase):
    def setUp(self):
        auth = UsernamePasswordAuth("username", "password")
        self.tamr = Client(auth)

    @responses.activate
    def test_delete(self):
        url = "http://localhost:9100/api/versioned/v1/datasets/1"
        responses.add(responses.GET, url, json=self._dataset_json)
        responses.add(responses.DELETE, url, status=204)
        responses.add(responses.GET, url, status=404)

        dataset = self.tamr.datasets.by_resource_id("1")
        self.assertEqual(dataset._data, self._dataset_json)

        response = dataset.delete()
        self.assertEqual(response.status_code, 204)
        self.assertRaises(HTTPError, lambda: self.tamr.datasets.by_resource_id("1"))

    _dataset_json = {
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

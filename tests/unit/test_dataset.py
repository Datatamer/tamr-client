from functools import partial
import json
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
        responses.add(responses.GET, self._url, json=self._dataset_json)
        responses.add(responses.DELETE, self._url, status=204)
        responses.add(responses.GET, self._url, status=404)

        dataset = self.tamr.datasets.by_resource_id("1")
        self.assertEqual(dataset._data, self._dataset_json)

        response = dataset.delete()
        self.assertEqual(response.status_code, 204)
        self.assertRaises(HTTPError, lambda: self.tamr.datasets.by_resource_id("1"))

    @responses.activate
    def test_update(self):
        def create_callback(request, snoop):
            snoop["payload"] = request.body
            return 200, {}, json.dumps(self._updated_dataset_json)

        snoop_dict = {}
        responses.add(responses.GET, self._url, json=self._dataset_json)
        responses.add_callback(
            responses.PUT, self._url, partial(create_callback, snoop=snoop_dict)
        )

        dataset = self.tamr.datasets.by_resource_id("1")

        temp_spec = dataset.spec().with_description(
            self._updated_dataset_json["description"]
        )
        new_dataset = (
            temp_spec.with_external_id(self._updated_dataset_json["externalId"])
            .with_tags(self._updated_dataset_json["tags"])
            .put()
        )

        self.assertEqual(new_dataset._data, self._updated_dataset_json)
        self.assertEqual(json.loads(snoop_dict["payload"]), self._updated_dataset_json)
        self.assertEqual(dataset._data, self._dataset_json)

        # checking that intermediate didn't change
        self.assertEqual(
            temp_spec.to_dict()["externalId"], self._dataset_json["externalId"]
        )

    _url = "http://localhost:9100/api/versioned/v1/datasets/1"

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

    _updated_dataset_json = {
        "id": "unify://unified-data/v1/datasets/1",
        "externalId": "dataset1",
        "name": "dataset 1 name",
        "description": "updated description",
        "version": "dataset 1 version",
        "keyAttributeNames": ["tamr_id"],
        "tags": ["new", "tags"],
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

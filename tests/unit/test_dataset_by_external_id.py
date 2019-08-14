import json

import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

dataset_json = [
    {
        "id": "unify://unified-data/v1/datasets/1",
        "externalId": "number 1",
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

dataset_external_id = "number 1"
datasets_url = f"http://localhost:9100/api/versioned/v1/datasets?filter=externalId=={dataset_external_id}"


@responses.activate
def test_dataset_by_external_id__raises_when_not_found():
    responses.add(responses.GET, datasets_url, json=[])
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    with pytest.raises(KeyError):
        tamr.datasets.by_external_id(dataset_external_id)


@responses.activate
def test_dataset_by_external_id_succeeds():
    responses.add(responses.GET, datasets_url, json=dataset_json)
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    actual_dataset = tamr.datasets.by_external_id(dataset_external_id)
    assert actual_dataset._data == dataset_json[0]

from functools import partial
import json

import pytest
from requests import HTTPError
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@pytest.fixture
def client():
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    return tamr


@responses.activate
def test_delete(client):
    responses.add(responses.GET, _url, json=_dataset_json)
    responses.add(responses.DELETE, _url, status=204)
    responses.add(responses.GET, _url, status=404)

    dataset = client.datasets.by_resource_id("1")
    assert dataset._data == _dataset_json

    response = dataset.delete()
    assert response.status_code == 204
    with pytest.raises(HTTPError):
        client.datasets.by_resource_id("1")


@responses.activate
def test_cascading_delete(client):
    responses.add(responses.GET, _url, json=_dataset_json)
    responses.add(responses.DELETE, _url + "?cascade=True", status=204)
    responses.add(responses.GET, _url, status=404)

    dataset = client.datasets.by_resource_id("1")
    assert dataset._data == _dataset_json

    response = dataset.delete(cascade=True)
    assert response.status_code == 204
    with pytest.raises(HTTPError):
        client.datasets.by_resource_id("1")


@responses.activate
def test_update(client):
    def create_callback(request, snoop):
        snoop["payload"] = request.body
        return 200, {}, json.dumps(_updated_dataset_json)

    snoop_dict = {}
    responses.add(responses.GET, _url, json=_dataset_json)
    responses.add_callback(
        responses.PUT, _url, partial(create_callback, snoop=snoop_dict)
    )

    dataset = client.datasets.by_resource_id("1")

    temp_spec = dataset.spec().with_description(_updated_dataset_json["description"])
    new_dataset = (
        temp_spec.with_external_id(_updated_dataset_json["externalId"])
        .with_tags(_updated_dataset_json["tags"])
        .put()
    )

    assert new_dataset._data == _updated_dataset_json
    assert json.loads(snoop_dict["payload"]) == _updated_dataset_json
    assert dataset._data == _dataset_json

    # checking that intermediate didn't change
    assert temp_spec.to_dict()["externalId"] == _dataset_json["externalId"]


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

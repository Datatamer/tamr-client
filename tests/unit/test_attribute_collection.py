import pytest
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@pytest.fixture
def client():
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    return tamr


@responses.activate
def test_delete_by_resource_id(client):
    ds_url = url_prefix + "datasets/7"
    attr_url = ds_url + "/attributes/family_role"

    responses.add(responses.GET, ds_url, json=datasets_collection[0])
    responses.add(responses.DELETE, attr_url, status=204)

    attributes = client.datasets.by_resource_id("7").attributes
    response = attributes.delete_by_resource_id("family_role")
    assert response.status_code == 204


url_prefix = "http://localhost:9100/api/versioned/v1/"

datasets_collection = [
    {
        "id": "unify://unified-data/v1/datasets/115",
        "name": "Globex_Store_Customers",
        "description": "",
        "version": "659",
        "keyAttributeNames": ["custid"],
        "tags": [],
        "created": {
            "username": "admin",
            "time": "2019-08-02T20:11:51.643Z",
            "version": "23388",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-08-08T18:18:14.047Z",
            "version": "26090",
        },
        "relativeId": "datasets/115",
        "upstreamDatasetIds": [],
        "externalId": "05d15bfd-d709-472a-ad5a-048e3367cfab",
    }
]

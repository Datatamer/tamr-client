import json

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

status_json = {
    "datasetName": "ds1",
    "relativeDatasetId": "v1/datasets/1",
    "isStreamable": True,
}


@responses.activate
def test_dataset_status():
    dataset_id = "1"
    dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/{dataset_id}"
    status_url = f"{dataset_url}/status"
    responses.add(responses.GET, dataset_url, json={})
    responses.add(responses.GET, status_url, json=status_json)
    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)

    dataset = tamr.datasets.by_resource_id(dataset_id)
    status = dataset.status()
    assert status._data == status_json

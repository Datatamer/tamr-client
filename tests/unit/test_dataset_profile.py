import json

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

profile_json1 = {
    "datasetName": "ds3",
    "relativeDatasetId": "v1/datasets/3",
    "isUpToDate": "false",
    "profiledDataVersion": "3",
    "profiledAt": {
        "username": "system",
        "time": "2019-06-05T14:23:25.860Z",
        "version": "46",
    },
    "simpleMetrics": [{"metricName": "rowCount", "metricValue": "1999"}],
}


@responses.activate
def test_dataset_profile():
    dataset_id = "3"
    dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/{dataset_id}"
    profile_url = f"{dataset_url}/profile"
    profile_refresh_url = f"{profile_url}:refresh"
    responses.add(responses.GET, dataset_url, json={})
    responses.add(responses.GET, profile_url, json=profile_json1)
    responses.add(responses.POST, profile_refresh_url, json=[], status=204)
    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)

    dataset = unify.datasets.by_resource_id(dataset_id)
    profile = dataset.profile()
    assert profile._data == profile_json1

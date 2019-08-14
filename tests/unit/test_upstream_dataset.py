import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@responses.activate
def test_upstream_dataset():

    dataset_json = {
        "id": "unify://unified-data/v1/datasets/12",
        "name": "Project_1_unified_dataset_dedup_features",
        "description": "Features for all the rows and values in the source dataset. Used in Dedup Workflow.",
        "version": "543",
        "keyAttributeNames": ["entityId"],
        "tags": [],
        "created": {
            "username": "admin",
            "time": "2019-06-05T18:31:59.327Z",
            "version": "212",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-07-18T14:19:28.133Z",
            "version": "22225",
        },
        "relativeId": "datasets/12",
        "upstreamDatasetIds": ["unify://unified-data/v1/datasets/8"],
        "externalId": "Project_1_unified_dataset_dedup_features",
    }

    upstream_json = ["unify://unified-data/v1/datasets/8"]

    upstream_ds_json = {
        "id": "unify://unified-data/v1/datasets/8",
        "name": "Project_1_unified_dataset",
        "description": "",
        "version": "529",
        "keyAttributeNames": ["tamr_id"],
        "tags": [],
        "created": {
            "username": "admin",
            "time": "2019-06-05T16:28:11.639Z",
            "version": "83",
        },
        "lastModified": {
            "username": "admin",
            "time": "2019-07-22T20:31:23.968Z",
            "version": "23146",
        },
        "relativeId": "datasets/8",
        "upstreamDatasetIds": ["unify://unified-data/v1/datasets/6"],
        "externalId": "Project_1_unified_dataset",
        "resourceId": "8",
    }

    tamr = Client(UsernamePasswordAuth("username", "password"))

    url_prefix = "http://localhost:9100/api/versioned/v1/"
    dataset_url = url_prefix + "datasets/12"
    upstream_url = url_prefix + "datasets/12/upstreamDatasets"
    upstream_ds_url = url_prefix + "datasets/8"

    responses.add(responses.GET, dataset_url, json=dataset_json)
    responses.add(responses.GET, upstream_url, json=upstream_json)
    responses.add(responses.GET, upstream_ds_url, json=upstream_ds_json)

    project_ds = tamr.datasets.by_relative_id("datasets/12")
    actual_upstream_ds = project_ds.upstream_datasets()
    uri_dataset = actual_upstream_ds[0].dataset()

    assert actual_upstream_ds[0].relative_id == upstream_ds_json["relativeId"]
    assert actual_upstream_ds[0].resource_id == upstream_ds_json["resourceId"]
    assert uri_dataset.name == upstream_ds_json["name"]

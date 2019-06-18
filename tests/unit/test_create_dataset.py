import json

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

auth = UsernamePasswordAuth("username", "password")
unify = Client(auth)


@responses.activate
def test_create_dataset():
    dataset_creation_spec = {
        "id": "unify://unified-data/v1/datasets/1",
        "name": "dataset",
        "keyAttributeNames": ["F1"],
        "description": "So much data in here!",
        "externalId": "Dataset created with pubapi",
    }

    datasets_url = f"http://localhost:9100/api/versioned/v1/datasets"
    dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"

    responses.add(responses.POST, datasets_url, json=dataset_creation_spec, status=204)
    responses.add(responses.GET, dataset_url, json=dataset_creation_spec)

    u = unify.create_dataset(dataset_creation_spec)
    p = unify.datasets.by_resource_id("1")
    assert u.name == p.name
    assert u.key_attribute_names == p.key_attribute_names
    assert u.description == p.description
    assert u.external_id == p.external_id

import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

auth = UsernamePasswordAuth("username", "password")
unify = Client(auth)


@responses.activate
def test_dataset_attributes():
    attribute_creation_spec = {
        "name": "myAttribute",
        "description": "",
        "type": {"baseType": "STRING", "attributes": []},
        "isNullable": "false",
    }

    dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/1"

    responses.add(responses.GET, dataset_url, json={})
    responses.add(
        responses.POST,
        dataset_url + "/attributes",
        json=attribute_creation_spec,
        status=204,
    )
    responses.add(
        responses.GET,
        dataset_url + "/attributes/myAttribute",
        json=attribute_creation_spec,
    )

    dataset = unify.datasets.by_resource_id("1")
    create = dataset.attributes.create(attribute_creation_spec)
    created = dataset.attributes.by_name("myAttribute")

    assert (create.relative_id) == (created.relative_id)
    assert (create.name) == (created.name)
    assert (create.type.base_type) == (created.type.base_type)

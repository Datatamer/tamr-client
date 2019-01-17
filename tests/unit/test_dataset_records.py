import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@responses.activate
def test_dataset_records():
    dataset_id = "1"
    dataset_url = f"http://localhost:9100/api/versioned/v1/datasets/{dataset_id}"
    records_url = f"{dataset_url}/records"
    responses.add(responses.GET, dataset_url, json={})
    responses.add(
        responses.GET, records_url, body='{"attribute1": 1}\n{"attribute1": 2}'
    )
    auth = UsernamePasswordAuth("username", "password")
    unify = Client(auth)

    dataset = unify.datasets.by_resource_id(dataset_id)
    records = list(dataset.stream_records())
    assert records == [{"attribute1": 1}, {"attribute1": 2}]

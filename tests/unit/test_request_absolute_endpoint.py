import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@responses.activate
def test_request_absolute_endpoint():
    endpoint = "/api/service/health"
    full_url = f"http://localhost:9100{endpoint}"
    responses.add(responses.GET, full_url, json={})

    client = Client(UsernamePasswordAuth("username", "password"))

    # If client does not properly handle absolute paths, client.get() will
    # raise a ConnectionRefused exception.
    response = client.get(endpoint)
    assert response.url == full_url

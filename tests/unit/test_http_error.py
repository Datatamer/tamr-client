from pytest import raises
from requests.exceptions import HTTPError
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@responses.activate
def test_http_error():
    """Ensure that the client surfaces HTTP errors as exceptions."""
    endpoint = "http://localhost:9100/api/versioned/v1/projects/1"
    responses.add(responses.GET, endpoint, status=401)
    auth = UsernamePasswordAuth("nonexistent-username", "invalid-password")
    tamr = Client(auth)
    with raises(HTTPError) as e:
        tamr.projects.by_resource_id("1")
    assert f"401 Client Error: Unauthorized for url: {endpoint}" in str(e)

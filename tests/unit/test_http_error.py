import responses
from requests.exceptions import HTTPError
import pytest

from tamr_unify_client.auth import UsernamePasswordAuth
from tamr_unify_client import Client


@responses.activate
def test_http_error():
    """Ensure that the client surfaces HTTP errors as exceptions.
    """
    endpoint = f"http://localhost:9100/api/versioned/v1/projects/1"
    responses.add(responses.GET, endpoint, status=401)
    auth = UsernamePasswordAuth("nonexistent-username", "invalid-password")
    unify = Client(auth)
    with pytest.raises(HTTPError) as e:
        unify.projects.by_resource_id("1")
    assert f"401 Client Error: Unauthorized for url: {endpoint}" in str(e)

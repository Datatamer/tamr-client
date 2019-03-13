import requests
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


@responses.activate
def test_request_session_cookie():
    endpoint = "http://localhost:9100/api/versioned/v1/test"
    responses.add(responses.GET, endpoint, json={})

    session = requests.Session()
    cookie = requests.cookies.create_cookie(
        name="test_cookie", value="the-cookie-works"
    )
    session.cookies.set_cookie(cookie)

    client = Client(UsernamePasswordAuth("username", "password"), session=session)

    assert client.session is session

    endpoint = "test"
    client.get(endpoint)

    assert len(responses.calls) == 1
    req = responses.calls[0].request
    assert req.url.endswith("test")
    assert req.headers.get("Cookie") is not None
    assert "test_cookie=" in req.headers.get("Cookie")

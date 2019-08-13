import responses


from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth


auth = UsernamePasswordAuth("username", "password")

"""
This is a test file for testing imperfect base paths, and various other tests too.
The first five tests demonstrate that the client can handle badly written base paths and produce correct final urls.
Each test runs a request to the server, and produces the correct final url.
"""


@responses.activate
def test_base_path_no_trailing_slash():
    bad_base_path = "/api/versioned/v1"
    tamr = Client(auth, base_path=bad_base_path)
    full_url = "http://localhost:9100/api/versioned/v1/datasets/1"
    responses.add(responses.GET, full_url, status=200)
    tamr.get("datasets/1")


@responses.activate
def test_base_path_no_leading_slash():
    bad_base_path = "api/versioned/v1/"
    tamr = Client(auth, base_path=bad_base_path)
    full_url = "http://localhost:9100/api/versioned/v1/datasets/1"
    responses.add(responses.GET, full_url, status=200)
    tamr.get("datasets/1")


@responses.activate
def test_base_path_no_slash():
    bad_base_path = "api/versioned/v1"
    tamr = Client(auth, base_path=bad_base_path)
    full_url = "http://localhost:9100/api/versioned/v1/datasets/1"
    responses.add(responses.GET, full_url, status=200)
    tamr.get("datasets/1")


@responses.activate
def test_base_path_default_slash():
    standard_base_path = "/api/versioned/v1/"
    tamr = Client(auth, base_path=standard_base_path)
    full_url = "http://localhost:9100/api/versioned/v1/datasets/1"
    responses.add(responses.GET, full_url, status=200)
    tamr.get("datasets/1")


@responses.activate
def test_base_path_no_base_path():
    tamr = Client(auth)
    full_url = "http://localhost:9100/api/versioned/v1/datasets/2"
    responses.add(responses.GET, full_url, status=400)
    tamr.get("datasets/2")


@responses.activate
def test_request_absolute_endpoint():
    endpoint = "/api/service/health"
    full_url = f"http://localhost:9100{endpoint}"
    responses.add(responses.GET, full_url, json={})
    client = Client(UsernamePasswordAuth("username", "password"))
    # If client does not properly handle absolute paths, client.get() will
    # raise a ConnectionRefused exception.
    client.get(endpoint)

from functools import partial
import json

import pytest
import requests
import responses

from tamr_unify_client import Client
from tamr_unify_client.auth import TokenAuth, UsernamePasswordAuth

auth_json = {
    "token": "auth_token_string_value",
    "username": "username",
}

expired_auth_json = {"token": "expired_auth_token", "user": "username"}


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


@responses.activate
def test_auth_cookie():
    def create_callback(request, snoop, status, response_body):
        snoop["headers"] = request.headers
        snoop["body"] = json.loads(request.body) if request.body is not None else None
        return status, {}, json.dumps(response_body)

    auth_endpoint = "http://localhost:9100/api/versioned/v1/instance:login"
    snoop_dict = {}
    responses.add_callback(
        responses.POST,
        auth_endpoint,
        partial(create_callback, snoop=snoop_dict, status=200, response_body=auth_json),
    )

    auth = UsernamePasswordAuth("user", "password")
    client = Client(auth, store_auth_cookie=True)

    assert client.auth == auth
    assert client.session.auth is None
    assert snoop_dict["body"] == {"username": "user", "password": "password"}
    assert client.session.cookies.get("authToken") == auth_json["token"]

    # Ensure credentials are not passed on subsequent requests
    endpoint = "http://localhost:9100/api/versioned/v1/test"
    snoop_dict = {}
    responses.add_callback(
        responses.GET,
        endpoint,
        partial(create_callback, snoop=snoop_dict, status=200, response_body={}),
    )

    client.get(endpoint)

    # No credentials, but valid cookie passed in second call
    assert "Authorization" not in snoop_dict["headers"]
    assert snoop_dict["headers"]["Cookie"] == f'authToken={auth_json["token"]}'


@responses.activate
def test_auth_cookie_refresh():
    def create_callback(request, snoop, status, response_body):
        snoop["headers"] = request.headers
        snoop["body"] = json.loads(request.body) if request.body is not None else None
        return status, {}, json.dumps(response_body)

    # First hit auth endpoint on client creation
    auth_endpoint = "http://localhost:9100/api/versioned/v1/instance:login"
    snoop_dict = {}
    responses.add_callback(
        responses.POST,
        auth_endpoint,
        partial(
            create_callback,
            snoop=snoop_dict,
            status=200,
            response_body=expired_auth_json,
        ),
    )

    auth = UsernamePasswordAuth("user", "password")
    client = Client(auth, store_auth_cookie=True)

    assert client.auth == auth
    assert client.session.auth is None
    assert snoop_dict["body"] == {"username": "user", "password": "password"}
    assert client.session.cookies.get("authToken") == expired_auth_json["token"]

    # Clear responses
    responses.reset()

    # Next hit target endpoint but credentials are expired
    endpoint = "http://localhost:9100/api/versioned/v1/test"
    snoop_dict_1 = {}
    responses.add_callback(
        responses.GET,
        endpoint,
        partial(
            create_callback,
            snoop=snoop_dict_1,
            status=401,
            response_body="Credentials are required to access this resource.",
        ),
    )

    # Hit auth endpoint again
    snoop_dict_2 = {}
    responses.add_callback(
        responses.POST,
        auth_endpoint,
        partial(
            create_callback, snoop=snoop_dict_2, status=200, response_body=auth_json,
        ),
    )

    # Finally hit target endpoint and succeed
    snoop_dict_3 = {}
    responses.add_callback(
        responses.GET,
        endpoint,
        partial(create_callback, snoop=snoop_dict_3, status=200, response_body={}),
    )

    r = client.get(endpoint)
    # Final response should succeed
    assert r.status_code == 200
    # Session should have refreshed cookie
    assert client.auth == auth
    assert client.session.auth is None
    assert client.session.cookies.get("authToken") == auth_json["token"]

    # Check headers from each call
    # No credentials in any call
    assert "Authorization" not in snoop_dict_1["headers"]
    assert "Authorization" not in snoop_dict_2["headers"]
    assert "Authorization" not in snoop_dict_3["headers"]
    # Expired cookie in first call
    assert (
        snoop_dict_1["headers"]["Cookie"] == f'authToken={expired_auth_json["token"]}'
    )
    # Credentials passed to auth service
    assert snoop_dict["body"] == {"username": "user", "password": "password"}
    # No credentials, but valid cookie passed in second call
    assert snoop_dict_3["headers"]["Cookie"] == f'authToken={auth_json["token"]}'


def test_auth_cookie_token_auth_not_supported():
    auth = TokenAuth("token")
    with pytest.raises(TypeError):
        Client(auth, store_auth_cookie=True)

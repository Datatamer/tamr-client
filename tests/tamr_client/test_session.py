from functools import partial
import json

import pytest
import requests
import responses

import tamr_client as tc
from tests.tamr_client import fake


@fake.json
def test_get_auth_cookie():
    auth = fake.username_password_auth()
    s = fake.session()
    instance = fake.instance()

    assert s.auth is None
    assert s._stored_auth == auth
    assert len(s.cookies.keys()) == 0

    tc.backup.get_all(session=s, instance=instance)

    assert s.auth is None
    assert s._stored_auth == auth
    assert s.cookies.get("authToken") == "auth_token_string_value"


@fake.json
def test_refresh_auth_cookie():
    auth = fake.username_password_auth()
    s = fake.session()
    instance = fake.instance()

    assert s.auth is None
    assert s._stored_auth == auth
    assert len(s.cookies.keys()) == 0

    tc.backup.get_all(session=s, instance=instance)

    assert s.auth is None
    assert s._stored_auth == auth
    assert s.cookies.get("authToken") == "auth_token_string_value"


@fake.json
def test_bad_credentials():
    auth = fake.username_password_auth()
    s = fake.session()
    instance = fake.instance()

    assert s.auth is None
    assert s._stored_auth == auth
    assert len(s.cookies.keys()) == 0
    s.cookies.set("authToken", "expired_auth_token")

    with pytest.raises(requests.exceptions.HTTPError):
        tc.backup.get_all(session=s, instance=instance)


@fake.json
def test_missing_api():
    auth = fake.username_password_auth()
    s = fake.session()
    instance = fake.instance()

    assert s.auth is None
    assert s._stored_auth == auth
    assert len(s.cookies.keys()) == 0

    tc.backup.get_all(session=s, instance=instance)

    assert s.auth == auth


@responses.activate  # TODO: Can this request header checking be done with fake.json?
def test_request_headers():
    def create_callback(request, snoop, status, response_body):
        snoop["headers"] = request.headers
        return status, {}, json.dumps(response_body)

    auth_endpoint = "http://localhost/api/versioned/v1/instance:login"
    endpoint = "http://localhost/api/versioned/v1/backups"
    snoop_dict_1: tc._types.JsonDict = {}
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

    snoop_dict_2: tc._types.JsonDict = {}
    responses.add_callback(
        responses.POST,
        auth_endpoint,
        partial(
            create_callback, snoop=snoop_dict_2, status=200, response_body=auth_json
        ),
    )

    snoop_dict_3: tc._types.JsonDict = {}
    responses.add_callback(
        responses.GET,
        endpoint,
        partial(create_callback, snoop=snoop_dict_3, status=200, response_body={}),
    )

    s = fake.session()
    instance = fake.instance()
    tc.backup.get_all(session=s, instance=instance)

    # No credentials in any call
    assert "Authorization" not in snoop_dict_1["headers"]
    assert "Authorization" not in snoop_dict_2["headers"]
    assert "Authorization" not in snoop_dict_3["headers"]
    # No cookie in first call
    assert "Cookie" not in snoop_dict_1["headers"]
    # Valid cookie passed in second call
    assert snoop_dict_3["headers"]["Cookie"] == f'authToken={auth_json["token"]}'


auth_json = {"token": "auth_token_string_value", "username": "user"}

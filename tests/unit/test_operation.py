from urllib.parse import urljoin

import pytest
from requests import HTTPError
import responses


from tamr_unify_client.operation import Operation


@pytest.fixture
def client():
    from tamr_unify_client import Client
    from tamr_unify_client.auth import UsernamePasswordAuth

    auth = UsernamePasswordAuth("username", "password")
    tamr = Client(auth)
    return tamr


def full_url(client, endpoint):
    return urljoin(client.origin + client.base_path, endpoint)


op_1_json = {
    "id": "1",
    "type": "SPARK",
    "description": "Profiling [dataset] attributes.",
    "status": {
        "state": "SUCCEEDED",
        "startTime": "2019-08-28T18:51:06.856Z",
        "endTime": "2019-08-28T18:53:08.204Z",
        "message": "",
    },
    "created": {
        "username": "admin",
        "time": "2019-08-28T18:50:35.582Z",
        "version": "17",
    },
    "lastModified": {
        "username": "system",
        "time": "2019-08-28T18:53:08.950Z",
        "version": "40",
    },
    "relativeId": "operations/1",
}


def test_operation_from_json(client):
    alias = "operations/123"
    op1 = Operation.from_json(client, op_1_json, alias)
    assert op1.api_path == alias
    assert op1.relative_id == op_1_json["relativeId"]
    assert op1.resource_id == "1"
    assert op1.type == op_1_json["type"]
    assert op1.description == op_1_json["description"]
    assert op1.status == op_1_json["status"]
    assert op1.state == "SUCCEEDED"
    assert op1.succeeded


@responses.activate
def test_operation_from_resource_id(client):
    responses.add(responses.GET, full_url(client, "operations/1"), json=op_1_json)

    op1 = Operation.from_resource_id(client, "1")

    assert op1.resource_id == "1"
    assert op1.succeeded


@responses.activate
def test_operation_from_response(client):
    responses.add(responses.GET, full_url(client, "operations/1"), json=op_1_json)

    op1 = Operation.from_response(client, client.get("operations/1").successful())

    assert op1.resource_id == "1"
    assert op1.succeeded


@responses.activate
def test_operation_from_response_noop(client):
    responses.add(responses.GET, full_url(client, "operations/2"), status=204)
    responses.add(responses.GET, full_url(client, "operations/-1"), status=404)

    op2 = Operation.from_response(client, client.get("operations/2").successful())

    assert op2.api_path is not None
    assert op2.relative_id is not None
    assert op2.resource_id is not None
    assert op2.type == "NOOP"
    assert op2.description is not None
    assert op2.status is not None
    assert op2.state == "SUCCEEDED"
    assert op2.succeeded

    op2a = op2.apply_options(asynchronous=True)
    assert op2a.succeeded

    op2w = op2a.wait()
    assert op2w.succeeded

    with pytest.raises(HTTPError):
        op2w.poll()

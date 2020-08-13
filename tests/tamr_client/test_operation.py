import pytest
import responses

import tamr_client as tc
from tests.tamr_client import fake, utils


def test_operation_from_json():
    url = tc.URL(path="operations/1")
    operation_json = utils.load_json("operation_succeeded.json")
    op = tc.operation._from_json(url, operation_json)
    assert op.url == url
    assert op.type == operation_json["type"]
    assert op.description == operation_json["description"]
    assert op.status == operation_json["status"]
    assert tc.operation.succeeded(op)


@responses.activate
def test_operation_from_url():
    s = fake.session()
    url = tc.URL(path="operations/1")

    operation_json = utils.load_json("operation_succeeded.json")
    responses.add(responses.GET, str(url), json=operation_json)

    op = tc.operation._from_url(s, url)
    assert op.url == url
    assert op.type == operation_json["type"]
    assert op.description == operation_json["description"]
    assert op.status == operation_json["status"]
    assert tc.operation.succeeded(op)


@responses.activate
def test_operation_from_response():
    s = fake.session()
    instance = fake.instance()
    url = tc.URL(path="operations/1")

    operation_json = utils.load_json("operation_succeeded.json")
    responses.add(responses.GET, str(url), json=operation_json)

    r = s.get(str(url))
    op = tc.operation._from_response(instance, r)
    assert op.url == url
    assert op.type == operation_json["type"]
    assert op.description == operation_json["description"]
    assert op.status == operation_json["status"]
    assert tc.operation.succeeded(op)


@responses.activate
def test_operation_from_response_noop():
    s = fake.session()
    instance = fake.instance()
    url = tc.URL(path="operations/2")
    responses.add(responses.GET, str(url), status=204)

    url_dummy = tc.URL(path="operations/-1")
    responses.add(responses.GET, str(url_dummy), status=404)

    r = s.get(str(url))
    op2 = tc.operation._from_response(instance, r)

    assert op2.url is not None
    assert op2.type == "NOOP"
    assert op2.description is not None
    assert op2.status is not None
    assert op2.status["state"] == "SUCCEEDED"
    assert tc.operation.succeeded(op2)

    op2w = tc.operation.wait(s, op2)
    assert tc.operation.succeeded(op2w)

    with pytest.raises(tc.operation.NotFound):
        tc.operation.poll(s, op2w)


@responses.activate
def test_from_resource_id():
    s = fake.session()
    instance = fake.instance()
    url = tc.URL(path="operations/1")

    operation_json = utils.load_json("operation_succeeded.json")
    responses.add(responses.GET, str(url), json=operation_json)

    resource_id = "1"
    op = tc.operation.from_resource_id(s, instance, resource_id)
    assert op.url == url
    assert op.type == operation_json["type"]
    assert op.description == operation_json["description"]
    assert op.status == operation_json["status"]
    assert tc.operation.succeeded(op)


@responses.activate
def test_operation_poll():
    s = fake.session()
    url = tc.URL(path="operations/1")

    pending_operation_json = utils.load_json("operation_pending.json")
    op1 = tc.operation._from_json(url, pending_operation_json)

    succeeded_operation_json = utils.load_json("operation_succeeded.json")
    responses.add(responses.GET, str(url), json=succeeded_operation_json)
    op2 = tc.operation.poll(s, op1)

    assert op2.url == op1.url
    assert not tc.operation.succeeded(op1)
    assert tc.operation.succeeded(op2)
